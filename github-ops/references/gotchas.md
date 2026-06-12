# 🐙 GitHub Operations: Gotchas & Anti-Patterns

GitHub CLI를 활용한 운영 수행 시 에이전트가 주의해야 할 사항입니다.

## 1. Auth Pitfalls (인증의 함정)
- **Expired Tokens**: `gh` CLI의 인증이 만료되었을 수 있습니다. 작업을 시작하기 전 `gh auth status`를 확인하십시오.
- **Scope Insufficiency**: 레포 생성이나 삭제 등 고권한 작업 시 토큰의 스코프가 부족하여 오류가 발생할 수 있습니다.

## 2. Resource Failures (자원 실패)
- **Private/Public Mismatch**: 대장의 의도와 달리 민감한 코드가 포함된 레포를 `Public`으로 생성하지 않도록 각별히 주의하십시오. (기본값은 `Private` 권장)
- **Spamming Issues**: 사소한 에러 하나하나를 모두 이슈로 등록하여 GitHub 저장소를 노이즈로 가득 채우지 마십시오.

## 3. Operational Errors (운영 오류)
- **PR Blind Merge**: PR을 생성하자마자 스스로 머지(Merge)해버리지 마십시오. 대장의 최종 리뷰를 기다리십시오.
- **Workflow Interruption**: GitHub Actions 등의 자동화 워크플로우를 충분히 이해하지 못한 채 환경 변수 등을 수정하여 빌드 파이프라인을 멈추게 하지 마십시오.

---
*Created by MS_Dev Third Gen Standard*
