import os
import itertools
import urllib.parse

BASE_URL = "https://daecheong-hue.netlify.app"
BRAND_NAME = "대청휴"
YOUTUBE_ID = "DxwimcJq3_A"

# 네이버 서치어드바이저 권장 글자수(타이틀 40자, 설명 80자 내외)에 맞춘 동적 SEO 데이터
SEO_VARIATIONS = itertools.cycle([
    {"kw": "출장마사지", "desc_point": "30분 내 신속 방문을 약속드립니다. 24시간 편안한 맞춤형 케어를 경험해보세요."},
    {"kw": "출장 아로마 마사지", "desc_point": "자택, 오피스텔 어디든 쾌속 배차됩니다. 지친 일상에 활력을 불어넣어 드립니다."},
    {"kw": "출장 케어 마사지", "desc_point": "전액 안심 후불제로 선입금 걱정 없이 편안하게 이용 가능한 전문 힐링 플랫폼입니다."},
    {"kw": "출장 스웨디시 마사지", "desc_point": "전문 테라피스트가 직접 방문하여 수준 높은 릴랙싱 케어를 선사합니다."},
    {"kw": "출장 바디케어 마사지", "desc_point": "언제든 부르시면 계신 곳으로 찾아갑니다. 스트레스와 피로를 한 번에 날려보세요."}
])

# 대청휴 업체 정보
SHOPS_DATA = [
    {
        "name": "대청휴 프리미엄",
        "phone": "0507-1280-3358",
        "desc": "전지역 30분 이내 방문 보장! 24시간 선입금 없는 100% 후불제 안심 케어",
        "price": "50,000원부터~",
        "score": "5.0",
        "img": "/images/shop1.jpg"
    }
]

# 충청권(대전 중심) 지역 데이터
REGION_DATA = {
    "daejeon": {
        "name": "대전광역시", "short": "대전",
        "districts": {
            "유성구": ["봉명동", "온천동", "구암동", "장대동", "상대동", "원신흥동", "도룡동", "신성동", "전민동", "관평동", "송강동", "노은동", "지족동", "반석동", "덕명동", "학하동", "진잠동"],
            "서구": ["둔산동", "탄방동", "월평동", "갈마동", "만년동", "괴정동", "용문동", "가장동", "내동", "변동", "도마동", "정림동", "복수동", "가수원동", "도안동", "관저동", "기성동"],
            "중구": ["은행동", "선화동", "대흥동", "문창동", "석교동", "대사동", "부사동", "용두동", "오류동", "태평동", "유천동", "문화동", "산성동"],
            "동구": ["중앙동", "신인동", "효동", "판암동", "용운동", "대동", "자양동", "가양동", "용전동", "성남동", "홍도동", "삼성동", "대청동", "산내동"],
            "대덕구": ["오정동", "대화동", "회덕동", "비래동", "송촌동", "중리동", "법동", "신탄진동", "석봉동", "덕암동", "목상동"]
        }
    },
    "cheongju": {
        "name": "청주시", "short": "청주",
        "districts": {
            "흥덕구": ["가경동", "복대동", "봉명동", "송정동", "강서동", "운천동", "신봉동", "오송읍", "강내면", "옥산면"],
            "청원구": ["율량동", "사천동", "오창읍", "내수읍", "우암동", "내덕동", "북이면"],
            "상당구": ["용암동", "금천동", "영운동", "탑대성동", "성안동", "중앙동", "용담동", "남일면", "문의면", "가덕면"],
            "서원구": ["사직동", "사창동", "모충동", "산남동", "분평동", "수곡동", "성화동", "개신동", "죽림동", "남이면", "현도면"]
        }
    },
    "sejong": {
        "name": "세종특별자치시", "short": "세종",
        "districts": {
            "세종시": ["나성동", "어진동", "새롬동", "다정동", "종촌동", "고운동", "아름동", "도담동", "보람동", "대평동", "소담동", "반곡동", "조치원읍", "장군면", "금남면", "부강면", "연서면"]
        }
    }
}

HTML_TEMPLATE = """<!doctype html>
<html lang="ko">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="robots" content="index,follow,max-image-preview:large">
  <meta name="Yeti" content="index,follow,max-image-preview:large">
  <title>{page_title}</title>
  <meta name="description" content="{meta_description}">
  <link rel="canonical" href="{canonical_url}">
  
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{brand}">
  <meta property="og:title" content="{page_title}">
  <meta property="og:description" content="{meta_description}">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:image" content="/images/gallery1.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- JSON-LD 구조화 데이터 동적 삽입 -->
  <script type="application/ld+json">
  {json_ld}
  </script>

  <style>
    :root {{
      --bg-dark: #1e1e24; --card-bg: #2b2b36; --card-inner: #1e1e24; --card-border: #3f3f4e;
      --text-main: #f4f4f5; --text-muted: #a1a1aa; --accent-color: #10b981; --accent-hover: #34d399;
      --star-color: #fbbf24;
      --font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Pretendard", Roboto, "Noto Sans KR", sans-serif;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ background-color: var(--bg-dark); color: var(--text-main); font-family: var(--font-family); line-height: 1.6; }}
    a {{ color: inherit; text-decoration: none; }}
    .wrap {{ max-width: 1040px; margin: 0 auto; padding: 0 16px; }}
    
    header.top {{ border-bottom: 1px solid var(--card-border); background: rgba(30, 30, 36, 0.96); position: sticky; top: 0; z-index: 100; backdrop-filter: blur(8px); }}
    .header-row {{ display: flex; align-items: center; justify-content: space-between; height: 64px; }}
    .brand {{ font-size: 1.4rem; font-weight: 800; letter-spacing: -0.5px; color: #fff; }}
    .brand span {{ color: var(--accent-color); }}
    .nav {{ display: flex; gap: 14px; font-size: 0.9rem; font-weight: 600; }}
    
    .page-head {{ padding: 24px 0 16px; }}
    .breadcrumbs {{ font-size: 0.82rem; color: var(--text-muted); margin-bottom: 8px; }}
    .breadcrumbs a:hover {{ text-decoration: underline; color: var(--accent-color); }}
    .title-line h1 {{ font-size: 1.75rem; font-weight: 800; margin-bottom: 4px; }}
    .page-description {{ font-size: 0.9rem; color: var(--text-muted); margin-top: 6px; line-height: 1.5; }}
    
    .star-summary-bar {{ display: inline-flex; flex-wrap: wrap; align-items: center; gap: 8px; background: var(--card-inner); border: 1px solid var(--card-border); padding: 8px 16px; border-radius: 20px; font-size: 0.85rem; margin-top: 14px; }}
    .star-summary-bar .stars {{ color: var(--star-color); font-weight: bold; }}
    
    .tags {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 16px 0 24px; }}
    .tag {{ background: var(--card-inner); border: 1px solid var(--card-border); padding: 6px 14px; border-radius: 20px; font-size: 0.85rem; transition: 0.2s; }}
    .tag:hover {{ border-color: var(--accent-color); color: #fff; background: var(--accent-color); }}
    
    .content-area {{ width: 100%; }}
    .panel {{ background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 12px; padding: 24px; margin-bottom: 20px; }}
    .panel h2 {{ font-size: 1.25rem; font-weight: 700; margin-bottom: 16px; color: #fff; border-left: 4px solid var(--accent-color); padding-left: 10px; }}
    
    .shop-list {{ display: flex; flex-direction: column; gap: 14px; margin-bottom: 10px; }}
    .shop-card-item {{ background: var(--card-inner); border: 1px solid var(--card-border); border-radius: 12px; padding: 16px; display: flex; gap: 16px; align-items: center; transition: 0.2s; }}
    .shop-card-item:hover {{ border-color: var(--accent-color); transform: translateY(-2px); }}
    .shop-card-item img {{ width: 120px; height: 120px; object-fit: cover; border-radius: 8px; flex-shrink: 0; }}
    .shop-card-info {{ flex: 1; min-width: 0; }}
    .shop-card-info h3 {{ font-size: 1.2rem; font-weight: 800; color: #fff; margin-bottom: 4px; display: flex; align-items: center; gap: 8px; }}
    .shop-card-info p {{ font-size: 0.9rem; color: var(--text-muted); margin-bottom: 10px; line-height: 1.4; }}
    .shop-card-bottom {{ display: flex; justify-content: space-between; align-items: center; }}
    .shop-card-bottom .price {{ color: var(--star-color); font-weight: 800; font-size: 1.1rem; }}
    .call-btn-mini {{ background: var(--accent-color); color: #fff; padding: 10px 18px; border-radius: 6px; font-size: 0.9rem; font-weight: bold; }}
    .call-btn-mini:hover {{ background: var(--accent-hover); }}
    
    /* 지역 맞춤 특징 박스 */
    .local-feature-box {{ background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 16px; margin-bottom: 16px; }}
    .local-feature-box p {{ font-size: 0.92rem; color: #e4e4e7; line-height: 1.6; margin: 0; }}
    .local-feature-box strong {{ color: var(--accent-color); }}
    
    /* 이용 후기 */
    .review-box {{ background: var(--card-inner); border: 1px solid var(--card-border); border-radius: 10px; padding: 16px; margin-bottom: 12px; }}
    .review-top {{ display: flex; justify-content: space-between; margin-bottom: 6px; }}
    .review-top strong {{ font-size: 0.9rem; color: #fff; }}
    .review-top span {{ font-size: 0.85rem; color: var(--star-color); font-weight: bold; }}
    .review-box p {{ font-size: 0.85rem; color: #d4d4d8; line-height: 1.5; margin: 0; }}
    
    /* 테이블 */
    .course-table {{ width: 100%; border-collapse: collapse; text-align: left; font-size: 0.92rem; margin-top: 10px; }}
    .course-table th, .course-table td {{ padding: 14px 14px; border-bottom: 1px solid var(--card-border); }}
    .course-table th {{ color: var(--text-muted); font-weight: 600; background: var(--card-inner); }}
    .course-table td:last-child {{ font-weight: 700; text-align: right; color: #fff; }}
    .course-desc {{ font-size: 0.82rem; color: var(--text-muted); display: block; margin-top: 4px; }}
    
    .media-container {{ display: flex; flex-direction: column; gap: 16px; }}
    .map-frame, .video-frame {{ width: 100%; height: 320px; border: 0; border-radius: 8px; }}
    
    footer {{ border-top: 1px solid var(--card-border); padding: 30px 0; text-align: center; color: var(--text-muted); font-size: 0.85rem; margin-top: 40px; }}
    @media (max-width: 768px) {{
      .shop-card-item {{ flex-direction: column; align-items: flex-start; }}
      .shop-card-item img {{ width: 100%; height: 180px; }}
      .call-btn-mini {{ width: 100%; text-align: center; margin-top: 10px; }}
      .shop-card-bottom {{ flex-direction: column; align-items: flex-start; gap: 10px; width: 100%; }}
    }}
  </style>
</head>
<body>
  <header class="top">
    <div class="wrap header-row">
      <a class="brand" href="/">대청<span>휴</span></a>
      <nav class="nav"><a href="/">홈으로</a></nav>
    </div>
  </header>

  <main id="main">
    <div class="wrap">
      <div class="page-head">
        <div class="breadcrumbs">{breadcrumbs}</div>
        <div class="title-line">
          <h1>{page_title_h1}</h1>
          <p class="page-description">{meta_description}</p>
        </div>
        <div class="star-summary-bar">
          <span class="stars">★★★★★ 5.0</span>
          <span>|</span>
          <span style="color: #34d399;">24시간 전지역 30분 빠른 방문</span>
          <span>|</span>
          <span style="color: #60a5fa;">선입금 0원 전액 안심 후불제</span>
        </div>
      </div>

      {tag_section}

      <div class="content-area">
        
        <!-- 동적 지역별 맞춤 방문 특징 섹션 (NEW) -->
        <section class="panel">
          <h2>{location_title} 지역 맞춤 방문 특징</h2>
          <div class="local-feature-box">
            <p>
              <strong>{location_title}</strong> 지역은 저희 대청휴의 주요 24시간 신속 배차 구역입니다. 복잡한 이동이나 주차 스트레스 없이, 현재 머무시는 자택이나 호텔, 오피스텔 등에서 바로 연락 주시면 됩니다. <strong>{location_title}</strong>의 지리에 밝은 베테랑 기사님과 전문 테라피스트가 30분 이내에 방문하여 그곳을 가장 쾌적한 프라이빗 힐링 공간으로 만들어 드립니다. 전액 후불제 운영으로 안심하고 편리하게 이용하세요.
            </p>
          </div>
        </section>

        <!-- 업체 목록 -->
        <section class="panel">
          <h2>{location_title} 추천 방문 케어</h2>
          <div class="shop-list">
            {shop_cards_html}
          </div>
        </section>
        
        <!-- 동적 지역명 치환 리뷰 섹션 -->
        <section class="panel">
          <h2>{location_title} 리얼 고객 이용 후기</h2>
          <div class="review-box">
            <div class="review-top">
              <strong>김*우 고객님 (자택 이용)</strong><span>★★★★★ 5.0</span>
            </div>
            <p>{location_title} 근처에서 회식 끝나고 자택에서 불렀는데, 늦은 새벽인데도 30분도 안 돼서 빠르게 와주셨습니다. 마사지 퀄리티도 샵 이상이고 선입금 없어서 편안하게 이용했습니다.</p>
          </div>
          <div class="review-box">
            <div class="review-top">
              <strong>이*진 고객님 (숙소 이용)</strong><span>★★★★★ 5.0</span>
            </div>
            <p>{location_title} 쪽에 출장 와서 숙소로 예약했습니다. 필요한 용품들 꼼꼼히 다 챙겨오시고, 관리사님 실력이 너무 부드럽고 시원해서 출장 피로가 다 날아갔네요. 대청휴 최고!</p>
          </div>
        </section>

        <!-- 코스 안내 -->
        <section class="panel">
          <h2>마사지 코스 및 요금 안내</h2>
          <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:16px;">어디서든 편안하게. 고객님께 맞는 최적의 힐링 코스를 선택해보세요.</p>
          <table class="course-table">
            <thead><tr><th>프로그램명 및 설명</th><th>이용시간</th><th>요금</th></tr></thead>
            <tbody>
              <tr>
                <td><strong>01 DRY (개운한 건식)</strong><span class="course-desc">오일 없이 전신 건식 지압과 스트레칭으로 굳은 근육을 시원하게 풀어주는 기본 코스.</span></td>
                <td>60분 / 90분 / 120분</td><td>50,000원 ~ 80,000원</td>
              </tr>
              <tr>
                <td><strong>02 AROMA (촉촉한 아로마)</strong><span class="course-desc">최고급 천연 아로마 오일을 사용하여 뭉친 근육을 부드럽게 이완하고 스트레스를 완화하는 릴랙싱 케어.</span></td>
                <td>60분 / 90분 / 120분</td><td>60,000원 ~ 90,000원</td>
              </tr>
              <tr>
                <td><strong>03 SPECIAL (스페셜 코스)</strong><span class="course-desc">아로마의 부드러움과 타이의 시원함, 집중 발관리까지 결합한 종합 집중 힐링 코스.</span></td>
                <td>120분 / 150분 / 180분</td><td>90,000원 ~ 150,000원</td>
              </tr>
              <tr>
                <td><strong>04 VIP SWEDISH (VIP 스웨디시)</strong><span class="course-desc">따뜻한 고급 수용성 오일과 부드러운 감성 테크닉으로 극상의 힐링을 선사하는 프리미엄 코스.</span></td>
                <td>60분 / 90분 / 120분</td><td>100,000원 ~ 150,000원</td>
              </tr>
            </tbody>
          </table>
        </section>

        <!-- 지도 및 영상 -->
        <section class="panel">
          <h2>{location_title} 배차 구역 및 안내 영상</h2>
          <div class="media-container">
            <iframe class="map-frame" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q={map_query}&output=embed" title="{location_title} 구글 지도"></iframe>
            <iframe class="video-frame" loading="lazy" src="https://www.youtube-nocookie.com/embed/{youtube_id}" title="대청휴 안내 영상" allowfullscreen></iframe>
          </div>
        </section>
      </div>
    </div>
  </main>

  <footer>
    <div class="wrap">
      <p>© 2026 {brand}. All Rights Reserved.</p>
      <p style="margin-top: 8px;">도메인: daecheong-hue.netlify.app</p>
    </div>
  </footer>
</body>
</html>
"""

def generate_shop_cards(location_name):
    cards = []
    for shop in SHOPS_DATA:
        cards.append(f"""
        <div class="shop-card-item">
          <img src="{shop['img']}" alt="{location_name} {shop['name']}">
          <div class="shop-card-info">
            <h3>{shop['name']} <span style="font-size:0.75rem; color:var(--star-color);">★ {shop['score']}</span></h3>
            <p>{shop['desc']}</p>
            <div class="shop-card-bottom">
              <span class="price">{shop['price']}</span>
              <a class="call-btn-mini" href="tel:{shop['phone']}">방문 예약 {shop['phone']}</a>
            </div>
          </div>
        </div>
        """)
    return "".join(cards)

def build_json_ld(brand, page_title_h1, meta_description, canonical_url):
    return f"""{{
      "@context": "https://schema.org",
      "@type": "HealthAndBeautyBusiness",
      "name": "{page_title_h1} - {brand}",
      "description": "{meta_description}",
      "url": "{canonical_url}",
      "telephone": "{SHOPS_DATA[0]['phone']}",
      "priceRange": "50,000원 ~ 150,000원",
      "aggregateRating": {{
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "345",
        "bestRating": "5",
        "worstRating": "1"
      }}
    }}"""

def make_page(path, html_content):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

urls = []
print(f"[{BRAND_NAME}] 사이트 대량 페이지 생성을 시작합니다 (지역별 특징+후기 최적화)...")

# ==========================================
# 0. 메인 페이지 생성 (루트 폴더)
# ==========================================
main_url = f"{BASE_URL}/"
urls.append(main_url)

# 사용자가 요청한 고정 메인 타이틀 및 설명
main_title = f"대전출장마사지 대청휴 | 24시간 전지역 빠른 방문 예약"
main_desc = f"대전 전지역 30분 내 방문이 가능한 대전출장마사지 전문플랫폼 대청휴입니다. 서구, 유성구, 중구 등 24시간 편안한 케어를 경험해보세요."

main_tags = "".join([f'<a class="tag" href="/region/{k}/">{v["name"]}</a>' for k, v in REGION_DATA.items()])

make_page(".", HTML_TEMPLATE.format(
    brand=BRAND_NAME, youtube_id=YOUTUBE_ID, map_query=urllib.parse.quote("대전 청주 세종"),
    page_title=main_title, page_title_h1="대전출장마사지 대청휴", 
    meta_description=main_desc, canonical_url=main_url, 
    json_ld=build_json_ld(BRAND_NAME, "대전출장마사지 대청휴", main_desc, main_url),
    location_title="충청권(대전/세종/청주)", breadcrumbs='홈',
    tag_section=f'<div class="tags">{main_tags}</div>', 
    shop_cards_html=generate_shop_cards("충청권")
))

# ==========================================
# 1~3. 지역별 페이지 생성 (시/도 -> 구/군 -> 동/읍/면)
# ==========================================
for reg_key, reg_val in REGION_DATA.items():
    reg_name = reg_val['name']
    
    # 1. 시/도 단위
    seo_data = next(SEO_VARIATIONS)
    reg_dir = os.path.join("region", reg_key)
    reg_url = f"{BASE_URL}/region/{reg_key}/"
    urls.append(reg_url)
    
    p_title = f"{reg_name} {seo_data['kw']} | {BRAND_NAME}"
    m_desc = f"{reg_name} {seo_data['kw']}. {seo_data['desc_point']}"
    p_h1 = f"{reg_name} {seo_data['kw']}"
    
    dist_tags = "".join([f'<a class="tag" href="/region/{reg_key}/{urllib.parse.quote(d_name)}/">{d_name}</a>' for d_name in reg_val['districts'].keys()])
    tag_html = f'<div class="tags">{dist_tags}</div>'
    
    make_page(reg_dir, HTML_TEMPLATE.format(
        brand=BRAND_NAME, youtube_id=YOUTUBE_ID, map_query=urllib.parse.quote(reg_name),
        page_title=p_title, page_title_h1=p_h1, meta_description=m_desc,
        canonical_url=reg_url, json_ld=build_json_ld(BRAND_NAME, p_title, m_desc, reg_url),
        location_title=reg_name, breadcrumbs=f'홈 › <a href="/">충청권</a> › {reg_name}',
        tag_section=tag_html, shop_cards_html=generate_shop_cards(reg_name)
    ))
    
    # 2. 구/군 단위
    for dist_name, dongs in reg_val['districts'].items():
        encoded_dist = urllib.parse.quote(dist_name)
        seo_data = next(SEO_VARIATIONS)
        dist_dir = os.path.join(reg_dir, dist_name)
        dist_url = f"{BASE_URL}/region/{reg_key}/{encoded_dist}/"
        urls.append(dist_url)
        
        full_dist_title = f"{reg_val['short']} {dist_name}"
        p_title = f"{full_dist_title} {seo_data['kw']} | {BRAND_NAME}"
        m_desc = f"{full_dist_title} {seo_data['kw']}. {seo_data['desc_point']}"
        p_h1 = f"{full_dist_title} {seo_data['kw']}"
        
        dong_tags = "".join([f'<a class="tag" href="/region/{reg_key}/{encoded_dist}/{urllib.parse.quote(d)}/">{d}</a>' for d in dongs])
        tag_html = f'<div class="tags">{dong_tags}</div>'
        
        make_page(dist_dir, HTML_TEMPLATE.format(
            brand=BRAND_NAME, youtube_id=YOUTUBE_ID, map_query=urllib.parse.quote(full_dist_title),
            page_title=p_title, page_title_h1=p_h1, meta_description=m_desc,
            canonical_url=dist_url, json_ld=build_json_ld(BRAND_NAME, p_title, m_desc, dist_url),
            location_title=full_dist_title,
            breadcrumbs=f'홈 › <a href="/region/{reg_key}/">{reg_name}</a> › {dist_name}',
            tag_section=tag_html, shop_cards_html=generate_shop_cards(full_dist_title)
        ))
        
        # 3. 동/읍/면 단위
        for dong in dongs:
            encoded_dong = urllib.parse.quote(dong)
            seo_data = next(SEO_VARIATIONS)
            dong_dir = os.path.join(dist_dir, dong)
            dong_url = f"{BASE_URL}/region/{reg_key}/{encoded_dist}/{encoded_dong}/"
            urls.append(dong_url)
            
            full_dong_title = f"{reg_val['short']} {dist_name} {dong}"
            p_title = f"{full_dong_title} {seo_data['kw']} | {BRAND_NAME}"
            m_desc = f"{full_dong_title} {seo_data['kw']}. {seo_data['desc_point']}"
            p_h1 = f"{full_dong_title} {seo_data['kw']}"
            
            make_page(dong_dir, HTML_TEMPLATE.format(
                brand=BRAND_NAME, youtube_id=YOUTUBE_ID, map_query=urllib.parse.quote(full_dong_title),
                page_title=p_title, page_title_h1=p_h1, meta_description=m_desc,
                canonical_url=dong_url, json_ld=build_json_ld(BRAND_NAME, p_title, m_desc, dong_url),
                location_title=full_dong_title,
                breadcrumbs=f'홈 › <a href="/region/{reg_key}/">{reg_name}</a> › <a href="/region/{reg_key}/{encoded_dist}/">{dist_name}</a> › {dong}',
                tag_section="", shop_cards_html=generate_shop_cards(full_dong_title)
            ))

# ==========================================
# 4. 사이트맵 및 robots.txt 생성
# ==========================================
sitemap_xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u in urls:
    sitemap_xml.append(f"  <url><loc>{u}</loc><priority>0.8</priority></url>")
sitemap_xml.append('</urlset>')

with open("sitemap.xml", "w", encoding="utf-8") as f:
    f.write("\n".join(sitemap_xml))

with open("robots.txt", "w", encoding="utf-8") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {BASE_URL}/sitemap.xml\n")

print(f"작업 완료! {BRAND_NAME} 사이트의 총 {len(urls)}개 페이지, sitemap.xml, robots.txt 생성이 완료되었습니다.")