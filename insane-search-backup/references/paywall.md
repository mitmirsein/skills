# Paywall Bypass & SEO Spoofing

> **Phase 1.5 전략**: 뉴스/미디어 매체의 페이월(Paywall)을 우회하기 위한 특수 설정. `insane-search`가 일반적인 방법으로 접근 시 "Subscribe to read" 류의 페이월을 만날 경우, 아래 규칙을 적용하여 재타격한다.

## 1. Domain-Strategy Mapping

### 1-1. Googlebot UA + XFF 타겟 (SEO 화이트리스트)
이 사이트들은 검색 엔진 크롤러에게 본문을 열어둔다.
*   **명령어**: `curl -sL -H "User-Agent: Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" -H "X-Forwarded-For: 66.249.66.1" -H "Referer: https://www.google.com/" -b "" "{URL}"`
*   **대상 도메인**: `wsj.com`, `barrons.com`, `ft.com`, `economist.com`, `theaustralian.com.au`, `thetimes.co.uk`, `telegraph.co.uk`, `zeit.de`, `handelsblatt.com`, `leparisien.fr`, `nzz.ch`, `usatoday.com`, `quora.com`, `lefigaro.fr`, `lemonde.fr`, `spiegel.de`, `sueddeutsche.de`, `frankfurter-allgemeine.de`, `wires.com`, `brisbanetimes.com.au`, `smh.com.au`, `theage.com.au`

### 1-2. Bingbot UA 타겟
*   **명령어**: `curl -sL -H "User-Agent: Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)" -H "Referer: https://www.bing.com/" -b "" "{URL}"`
*   **대상 도메인**: `haaretz.com`, `nzherald.co.nz`, `stratfor.com`, `themarker.com`

### 1-3. AMP 폴백 타겟
위의 크롤러 위장이 안 먹히면 AMP 모바일 버전을 시도한다. (페이월이 약하게 적용됨)
*   **방법**: URL 끝에 `/amp`, `?outputType=amp`, `.amp.html`, `?amp` 중 하나를 붙여서 시도.
*   **대상 도메인**: `wsj.com`, `bostonglobe.com`, `latimes.com`, `chicagotribune.com`, `seattletimes.com`, `theatlantic.com`, `wired.com`, `newyorker.com`, `washingtonpost.com`, `smh.com.au`, `theage.com.au`, `brisbanetimes.com.au`

### 1-4. 소셜 Referer 타겟
SNS 공유 유입은 페이월을 풀어주는 사이트.
*   **명령어 (Facebook)**: 일반 브라우저 UA + `-H "Referer: https://www.facebook.com/"`
*   **대상 도메인 (Facebook)**: `law.com`, `ftm.nl`, `law360.com`, `sloanreview.mit.edu`
*   **명령어 (Twitter/X)**: 일반 브라우저 UA + `-H "Referer: https://t.co/"` (기타 미분류 범용 타겟에 폴백으로 사용 가능)

## 2. Paywall False-Positive Detection (페이월 잔류 감지)

정상적인 `200 OK` 응답이더라도, 가져온 텍스트가 사실은 **"구독 안내 메시지"**일 수 있다. 에이전트는 추출된 텍스트에서 아래 패턴을 검사해야 한다.

**감지 키워드 (정규식 / 대소문자 무시)**:
*   `subscribe to (continue|read|access|unlock)`
*   `paywall`
*   `premium[._]content`
*   `metered[._]paywall`
*   `article[._]limit`
*   `sign[._]in[._]to[._](continue|read)`
*   `create[._]a[._]free[._]account[._]to[._]unlock`
*   `membership[._]to[._]continue`
*   `subscribe now for full access`
*   `to continue reading`
*   `remaining free articles`
*   `subscribe or`
*   `already a subscriber`

👉 **조치**: 위 패턴이 감지되면 "추출 실패(페이월)"로 간주하고 즉시 `1-1` ~ `1-4`의 우회 전략으로 에스컬레이션 하거나, 최종적으로 `archive.today` 사이드카를 채택한다.

## 3. JSON-LD 파싱 우선 원칙

언론사 사이트는 페이월로 HTML 본문을 가리더라도 SEO를 위해 `<script type="application/ld+json">` 태그 안에 `articleBody` 필드로 전문을 숨겨놓는 경우가 많다.
따라서 HTML 응답을 받으면 항상 JSON-LD를 먼저 파싱하여 `articleBody` 존재 여부를 확인한다.
