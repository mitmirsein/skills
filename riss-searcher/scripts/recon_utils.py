"""
recon_utils.py — KCI/RISS Searcher Skills 공유 유틸리티

ForensicAudit, InsaneRecon(curl_cffi), LightpandaRecon 모듈을 제공합니다.
각 스킬의 scripts/ 디렉토리에서 공통으로 import됩니다.
"""

import os
import re
import subprocess
import logging

# 로깅 설정
logging.basicConfig(
    level=logging.WARNING,  # CLI 출력 오염 방지: WARNING 이상만
    format="%(levelname)s: %(message)s"
)
logger = logging.getLogger("recon_utils")

LIGHTPANDA_PATH = os.path.expanduser("~/Desktop/MS_Dev.nosync/bin/lightpanda")


class LightpandaRecon:
    """Lightpanda 바이너리 기반 동적 페이지 렌더링 정찰"""

    @staticmethod
    def fetch(url: str, wait_ms: int = 5000, dump_mode: str = "html") -> str | None:
        """Lightpanda로 JS 렌더링 후 HTML/텍스트 추출"""
        cmd = [
            LIGHTPANDA_PATH, "fetch",
            "--dump", dump_mode,
            "--strip-mode", "full",
            "--wait-ms", str(wait_ms),
            url
        ]
        try:
            logger.info(f"Lightpanda fetching: {url}")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=30)
            return result.stdout
        except subprocess.CalledProcessError as e:
            logger.warning(f"Lightpanda failed: {e.stderr[:200]}")
            return None
        except Exception as e:
            logger.warning(f"Lightpanda error: {e}")
            return None


class InsaneRecon:
    """curl_cffi 기반 TLS 핑거프린트 위장 — RISS WAF 우회 필수"""

    @staticmethod
    def fetch(url: str, impersonate: str = "safari15_5") -> str | None:
        """curl_cffi로 TLS 차단 우회"""
        try:
            from curl_cffi import requests as cffi_requests
            logger.info(f"InsaneRecon fetching: {url} (Impersonate: {impersonate})")
            response = cffi_requests.get(url, impersonate=impersonate, timeout=30)
            if response.status_code == 200:
                return response.text
            else:
                logger.warning(f"InsaneRecon status: {response.status_code}")
                return None
        except ImportError:
            logger.warning("curl_cffi 미설치 — InsaneRecon 사용 불가. httpx fallback으로 전환.")
            return None
        except Exception as e:
            logger.warning(f"InsaneRecon error: {e}")
            return None


class ForensicAudit:
    """
    검색 결과 제목에 쿼리 키워드가 실제로 포함되어 있는지 검증.
    
    띄어쓰기를 무시하는 엄격한 매칭으로 노이즈(관련 없는 논문)를 원천 차단.
    KCI의 'GET 무시 + 기본 목록 반환' 버그 감지에도 활용.
    """

    @staticmethod
    def verify_title(query: str, title: str) -> bool:
        """
        쿼리와 제목 간의 관련성을 3단계로 검증 (특수문자 및 불필요 접두사 대응)
        
        1단계: 공백 및 특수문자 제거 후 서브스트링 매칭 (한국어 붙여쓰기 처리)
        2단계: 원본 그대로 서브스트링 매칭
        3단계: 개별 키워드의 형태소/단어가 제목에 일부 포함되어 있는지 교집합 검사
        """
        if not query or not title:
            return False

        q_clean = query.lower().strip()
        t_clean = title.lower().strip()

        # 1단계: 공백 및 특수문자 제거 후 서브스트링 매칭
        q_norm = q_clean.replace(" ", "")
        t_norm = t_clean.replace(" ", "")
        q_alpha = re.sub(r"[^\w가-힣]", "", q_norm)
        t_alpha = re.sub(r"[^\w가-힣]", "", t_norm)

        if q_alpha and t_alpha and (q_alpha in t_alpha or t_alpha in q_alpha):
            return True

        # 2단계: 원본 서브스트링
        if q_clean in t_clean or t_clean in q_clean:
            return True

        # 3단계: 개별 단어 단위 매칭 (특수문자/문장부호 제외하고 2글자 이상인 단어 대상)
        q_words = [re.sub(r"[^\w가-힣]", "", w) for w in re.split(r"[\s,]+", q_clean) if len(re.sub(r"[^\w가-힣]", "", w)) >= 2]
        if q_words:
            # 쿼리의 유의미한 단어 중 하나라도 제목의 특수문자/공백 제거 본문에 부분 문자열로 포함되는지 확인
            if any(qw in t_alpha for qw in q_words if qw):
                return True

        return False

    @staticmethod
    def audit_results(query: str, results: list[dict], title_key: str = "title") -> tuple[list, list]:
        """
        결과 목록 전체를 감사하여 (통과, 실패) 튜플로 반환
        
        Returns:
            (verified, rejected): 각각 검증 통과/실패한 항목 목록
        """
        verified, rejected = [], []
        for item in results:
            title = item.get(title_key, "")
            if ForensicAudit.verify_title(query, title):
                verified.append(item)
            else:
                rejected.append(item)
        return verified, rejected
