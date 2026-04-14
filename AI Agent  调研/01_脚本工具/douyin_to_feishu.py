"""
抖音对标账号数据采集 → 飞书多维表格（完整版）

功能：
  1. collect  - 搜索抖音关键词，采集账号数据，过滤非AI垂类，写入飞书
  2. analyze  - 获取指定账号的详细视频数据并分析
  3. update   - 更新已有账号的最新粉丝数/获赞数等

用法：
  python3 douyin_to_feishu.py collect              # 采集新账号
  python3 douyin_to_feishu.py analyze 秋芝2046      # 分析指定账号
  python3 douyin_to_feishu.py update                # 更新所有账号数据
  python3 douyin_to_feishu.py collect --clean       # 清空旧数据后重新采集

环境变量（可选，不设则用默认值）：
  DOUYIN_COOKIE  - 抖音登录Cookie（过期需更新）
"""
import requests
import json
import time
import sys
import os
from datetime import datetime

# ============================================================
# 配置
# ============================================================

# 飞书应用凭证
FEISHU_APP_ID = "cli_a9572f59a3f81bd2"
FEISHU_APP_SECRET = "JJlj8YYRHVdekWsPpuQJbcHY5hBMDLGX"
FEISHU_APP_TOKEN = "CuiybJoOMafb9HsZbu2cfVhfnZg"
FEISHU_TABLE_ID = "tblLIHsNVlhfCEer"
FEISHU_URL = f"https://w5scrwkn9y.feishu.cn/base/{FEISHU_APP_TOKEN}?table={FEISHU_TABLE_ID}"

# 抖音Cookie（优先从环境变量读取）
DOUYIN_COOKIE = os.environ.get("DOUYIN_COOKIE", """passport_csrf_token=fd7e692aab3c009ef6c415c1e7f74f56; passport_csrf_token_default=fd7e692aab3c009ef6c415c1e7f74f56; enter_pc_once=1; UIFID_TEMP=c28de8733f1ee511ccb0564a01187da29dead71fe4bbd42555f601f82dee5714ad76726b4c651142e873391856c0ffe58e7d8e3b2224330f51521ac497ee1a97f1fe2c16f14dfe64bd6711d1632ddfb4; x-web-secsdk-uid=849f1f53-3f86-4bf5-9644-21d0fa95fcdc; hevc_supported=true; dy_swidth=1470; dy_sheight=956; fpk1=U2FsdGVkX1+SGhtqqUEgBsIP62iowFUhLgz4sWXC5FdiDzIFP01WtowTdnZfoM+aYglGB6FeeGJCwmLR2inPNg==; fpk2=02379953b93cd223243db09f1dd4e5b9; s_v_web_id=verify_mnsfq2zf_KHDJK8Mo_BTIw_4ebN_8fiF_BjTkFDE5JXG2; bd_ticket_guard_client_web_domain=2; is_dash_user=1; UIFID=c28de8733f1ee511ccb0564a01187da29dead71fe4bbd42555f601f82dee5714ad76726b4c651142e873391856c0ffe5892dde815d8b982bccbc89a69aceae0fceca78f4e62d849f56aced30ceedc6fad05bbd6b68794fc1ec78976fa8688a6000a69095c10bef49bedee1c6fff029e3602fe9138eb02b75d2c9f58e97b6f97163782d5b974ec3e387d70b9536d9fcdf7e68c16810cd446b9c7727246366c4fd; volume_info=%7B%22isUserMute%22%3Afalse%2C%22isMute%22%3Afalse%2C%22volume%22%3A0.5%7D; __ac_signature=_02B4Z6wo00f01K23f4QAAIDCniKJxIJ8q5Stl3sAAEK0ed; douyin.com; device_web_cpu_core=10; device_web_memory_size=8; strategyABtestKey=%221776142489.141%22; passport_mfa_token=CjeODeeQL9Ld6O7baysRPj06EB6GpPUhG6oOlNqfnHyRBMCP4IdOWpbNqm%2FzuUhZLxGAYiBOrm8VGkoKPAAAAAAAAAAAAABQTe50MTflBLyap70a7d8XzaiDKTLIo1YHYRycIxHx0ze%2B%2FklNfaNuOYj7q4HVxstc4hD%2B4o4OGPax0WwgAiIBAwVWGPE%3D; d_ticket=ea8956a7a3808238175bd263675983c7b5d3d; passport_assist_user=CkHVu2jY07OZG-L8jJoY2zsahU_dEhNh6AEMwKO-lc9sQejBBDxo5Peqk-LU2pB3h4dUIOItSXbLLWgPK5VuoYAITBpKCjwAAAAAAAAAAAAAUE0AuHY-KWZ-4iNEZ0Q5IEJ36bf_FnBEPuEAZz8Bgu34cW8aS63bGDD5fULgQdpS-akQv-OODhiJr9ZUIAEiAQNClEga; n_mh=QucieiwBoarcS0MhXmf91LS2P5Fg0nBd6GkSYKLrz-M; sid_guard=ac167701474af9e13e36acf04e0a060b%7C1776142549%7C5184000%7CSat%2C+13-Jun-2026+04%3A55%3A49+GMT; uid_tt=e160f81da73b0199c8dabaeb684ced03; uid_tt_ss=e160f81da73b0199c8dabaeb684ced03; sid_tt=ac167701474af9e13e36acf04e0a060b; sessionid=ac167701474af9e13e36acf04e0a060b; sessionid_ss=ac167701474af9e13e36acf04e0a060b; is_staff_user=false; has_biz_token=false; sid_ucp_v1=1.0.0-KDZhNWYxMjExMzNiMTNkMzE2MzM3YmMwYjI2NDljM2ViNTM5ODU2YTQKIQis68CrovXiAxDVkffOBhjvMSAMMMywie0FOAdA9AdIBBoCaGwiIGFjMTY3NzAxNDc0YWY5ZTEzZTM2YWNmMDRlMGEwNjBi; ssid_ucp_v1=1.0.0-KDZhNWYxMjExMzNiMTNkMzE2MzM3YmMwYjI2NDljM2ViNTM5ODU2YTQKIQis68CrovXiAxDVkffOBhjvMSAMMMywie0FOAdA9AdIBBoCaGwiIGFjMTY3NzAxNDc0YWY5ZTEzZTM2YWNmMDRlMGEwNjBi; _bd_ticket_crypt_cookie=01d63e735a26de48ed6f89c0102d6f1f; __security_mc_1_s_sdk_sign_data_key_web_protect=e867b29d-420a-a82a; __security_mc_1_s_sdk_cert_key=1dfb8aab-44a8-a988; __security_mc_1_s_sdk_crypt_sdk=b32352a4-48f7-9519; __security_server_data_status=1; login_time=1776142547607; publish_badge_show_info=%220%2C0%2C0%2C1776142551212%22; SelfTabRedDotControl=%5B%5D; ttwid=1%7CvZx4fCF5w0-FlHRTm92y1ZtGJFe7JQuqLpQxDnEoz2Q%7C1776142557%7Cc8927cf47bee5da8aabf4180b210a235c7c9bc80c36e7792311d15e648fdb5ec; my_rd=2; stream_recommend_feed_params=%22%7B%5C%22cookie_enabled%5C%22%3Atrue%2C%5C%22screen_width%5C%22%3A1470%2C%5C%22screen_height%5C%22%3A956%2C%5C%22browser_online%5C%22%3Atrue%2C%5C%22cpu_core_num%5C%22%3A10%2C%5C%22device_memory%5C%22%3A8%2C%5C%22downlink%5C%22%3A10%2C%5C%22effective_type%5C%22%3A%5C%224g%5C%22%2C%5C%22round_trip_time%5C%22%3A100%7D%22; download_guide=%223%2F20260414%2F1%22; odin_tt=4ba2efca7b34eba805675a4ed0634aae9cc47a605b4f9311c85f32060ed2246699919b9e7520409c824824c2c0033681126b4e0eee009dd9da0a0d1a8ef2eaa811abfee8f0e2d4ee67a879f94b1a370d; IsDouyinActive=true; home_can_add_dy_2_desktop=%221%22; msToken=; bit_env=xQ_cSEXsfDQJAwemUhQ0nKS4usWlnbNTDySupSMjtiP2wPs1Xes8g1JQcdavSBhEY6-rrM4C0_KzU_FYMkd01rTUQ_eOr_B9F2lo8JwOEs5PO0YlwbAjLi4hq2hNt3Zol3rBjYi4x0yWh2NdiDn1Q5AdBFQ68qCzsBBGugeUdrxs7quLKwiZUWelFcgPaIPXfV3hx4Sik-xAjYomkyVW-uIXG17Zu6NRZg_VpyxBPdikdFW1ETKKxyjJZkpevbIHikQVMnqwzRVFFjnAnVKuXzu4H-fqQkewxziX5xFbI_CaBY0L2NO6MtM8hXIrKmzHeBxTKSMHTTuLdVBQzVwaHyMIsglIFFDEwujgZZQVlkflhIepWVBOcAjm-Qa72fn_bK51kwkb_FPLd_pm8poLdGUTZw_5G3dYGw1FIEZ2OTeFQu8tbwYCb-__NZhbKeyC7XRnRN784hCDHMb_Wpbvk91kiSL__9ld2ls9PK6Sr28xkBP5znFuJ-YXqB5HgoUTE-aH8X9XS57qiZg5G-PZAh1kIoFyg6FJCLKr7cOo5dk%3D; gulu_source_res=eyJwX2luIjoiMmI1N2YyYzgxMDY5M2NmZGQ5NjU4ZmEzZDhiNzhmNGNjYTQxZjE5NjYwNTVhNTM5NzI4MDEzMDRhYTM5MGVjNiJ9; passport_auth_mix_state=ml09otvmcahusnkmybfaru5x3am3m6m1""")

# 搜索关键词
KEYWORDS = [
    'AI Agent企业',
    'AI智能体平台',
    'AI办公提效',
    'AI解决方案',
    'AI落地',
]

# AI垂类过滤词
AI_MUST_HAVE = [
    'ai', 'AI', 'Ai', '人工智能', '智能体', 'agent', 'Agent',
    'AIGC', 'aigc', '大模型', 'GPT', 'gpt', 'Claude', 'claude',
    '自动化', 'RPA', 'rpa', '数字员工', 'AI落地', 'AI解决方案',
    'AI办公', 'AI创业', 'AI工具', 'AI编程', 'coze', 'Coze',
    'dify', 'Dify', 'openclaw', 'OpenClaw', 'LLM',
]

EXCLUDE_KEYWORDS = [
    '央视', '新闻', '记者', '主持人', '财经主播', '选美',
    '建筑师', '美食', '旅行', '穿搭', '漫剧收徒', '带货',
    '房产', '律师', '医生', '健身', '减肥', '育儿',
]

# 关注级别映射
LEVEL_MAP = {
    "是-直接竞品": "⭐ 重点关注-直接竞品",
    "是-直接相关": "⭐ 重点关注-直接竞品",
    "是-大厂竞品": "⭐ 重点关注-直接竞品",
    "相关-行业KOL": "🔵 重要参考-行业KOL",
    "相关-AI趋势": "🔵 重要参考-行业KOL",
    "相关-AI趋势KOL": "🔵 重要参考-行业KOL",
    "相关-行业观察": "🔵 重要参考-行业KOL",
    "相关-垂直行业AI": "🟢 同类参考-垂直行业",
    "相关-AI培训": "🟢 同类参考-AI培训",
    "相关-AI创业者": "🟢 同类参考-AI创业",
    "相关-内容参考": "🟡 内容参考",
    "相关-AI开发者": "🟡 内容参考",
    "相关-AI产品": "🟡 内容参考",
}

DOUYIN_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Referer': 'https://www.douyin.com/',
    'Cookie': DOUYIN_COOKIE,
    'Accept': 'application/json, text/plain, */*',
}

TODAY = datetime.now().strftime("%Y-%m-%d")
DATA_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# 抖音 API
# ============================================================

def douyin_search(keyword, count=20):
    """搜索抖音视频"""
    url = 'https://www.douyin.com/aweme/v1/web/general/search/single/'
    params = {
        'device_platform': 'webapp', 'aid': '6383',
        'channel': 'channel_pc_web', 'search_channel': 'aweme_general',
        'keyword': keyword, 'search_source': 'normal_search',
        'query_correct_type': '1', 'is_filter_search': '0',
        'offset': '0', 'count': str(count),
        'version_code': '170400', 'version_name': '17.4.0',
        'cookie_enabled': 'true', 'platform': 'PC',
        'screen_width': '1470', 'screen_height': '956',
        'browser_language': 'zh-CN', 'browser_platform': 'MacIntel',
        'browser_name': 'Chrome', 'browser_version': '131.0.0.0',
        'browser_online': 'true', 'os_name': 'Mac OS',
        'os_version': '10.15.7', 'cpu_core_num': '10',
        'device_memory': '8', 'downlink': '10',
        'effective_type': '4g', 'round_trip_time': '100',
    }
    resp = requests.get(url, headers=DOUYIN_HEADERS, params=params)
    return resp.json().get('data', [])


def douyin_user_profile(sec_uid):
    """获取用户详细资料"""
    url = 'https://www.douyin.com/aweme/v1/web/user/profile/other/'
    params = {
        'device_platform': 'webapp', 'aid': '6383',
        'channel': 'channel_pc_web', 'sec_user_id': sec_uid,
        'version_code': '170400', 'version_name': '17.4.0',
        'cookie_enabled': 'true', 'platform': 'PC',
    }
    resp = requests.get(url, headers=DOUYIN_HEADERS, params=params)
    return resp.json().get('user', {})


def douyin_user_videos(sec_uid, count=20):
    """获取用户的视频列表"""
    url = 'https://www.douyin.com/aweme/v1/web/aweme/post/'
    params = {
        'device_platform': 'webapp', 'aid': '6383',
        'channel': 'channel_pc_web', 'sec_user_id': sec_uid,
        'max_cursor': '0', 'locate_item_id': '',
        'show_live_replay_strategy': '1', 'need_time_list': '1',
        'time_list_query': '0', 'whale_cut_token': '',
        'cut_version': '1', 'count': str(count),
        'publish_video_strategy_type': '2',
        'version_code': '170400', 'version_name': '17.4.0',
        'cookie_enabled': 'true', 'platform': 'PC',
    }
    resp = requests.get(url, headers=DOUYIN_HEADERS, params=params)
    return resp.json().get('aweme_list', [])


# ============================================================
# 飞书 API
# ============================================================

def feishu_token():
    """获取飞书 tenant_access_token"""
    url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
    resp = requests.post(url, json={"app_id": FEISHU_APP_ID, "app_secret": FEISHU_APP_SECRET})
    return resp.json()["tenant_access_token"]


def feishu_headers(token):
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def feishu_get_records(token):
    """获取所有记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records"
    headers = feishu_headers(token)
    all_items = []
    page_token = None
    while True:
        params = {"page_size": 100}
        if page_token:
            params["page_token"] = page_token
        resp = requests.get(url, headers=headers, params=params)
        data = resp.json()
        all_items.extend(data.get("data", {}).get("items", []))
        if not data.get("data", {}).get("has_more", False):
            break
        page_token = data["data"]["page_token"]
    return all_items


def feishu_create_records(token, records):
    """批量创建记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records/batch_create"
    body = {"records": [{"fields": r} for r in records]}
    resp = requests.post(url, headers=feishu_headers(token), json=body)
    return resp.json()


def feishu_update_record(token, record_id, fields):
    """更新单条记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records/{record_id}"
    resp = requests.put(url, headers=feishu_headers(token), json={"fields": fields})
    return resp.json()


def feishu_delete_records(token, record_ids):
    """批量删除记录"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/records/batch_delete"
    for i in range(0, len(record_ids), 500):
        batch = record_ids[i:i+500]
        requests.post(url, headers=feishu_headers(token), json={"records": batch})


def feishu_add_field(token, field_name, field_type=1):
    """添加字段（已存在会跳过）"""
    url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{FEISHU_APP_TOKEN}/tables/{FEISHU_TABLE_ID}/fields"
    requests.post(url, headers=feishu_headers(token),
                  json={"field_name": field_name, "type": field_type})


# ============================================================
# 工具函数
# ============================================================

def is_ai_account(nickname, signature):
    """判断是否为AI垂类账号"""
    text = f"{nickname} {signature}".lower()
    for ex in EXCLUDE_KEYWORDS:
        if ex.lower() in text:
            return False
    for kw in AI_MUST_HAVE:
        if kw.lower() in text:
            return True
    return False


def account_type(user):
    """判断账号类型"""
    if user.get('enterprise_verify_reason'):
        return '企业号'
    elif user.get('custom_verify'):
        return '个人认证'
    elif user.get('verification_type', 0) > 0:
        return '认证号'
    return '个人号'


def format_count(n):
    if n >= 10000:
        return f"{n/10000:.1f}万"
    return str(n)


def get_existing_names(token):
    """获取飞书表格中已有的账号名称"""
    records = feishu_get_records(token)
    names = set()
    for item in records:
        name = item.get("fields", {}).get("账号名称", "")
        if isinstance(name, list):
            name = name[0].get("text", "") if name else ""
        if name:
            names.add(name)
    return names


# ============================================================
# 命令: collect - 采集新账号
# ============================================================

def cmd_collect(clean=False):
    print("=" * 60)
    print(f"  抖音对标账号采集 → 飞书  [{TODAY}]")
    print("=" * 60)

    # 1. 搜索
    print(f"\n[1/4] 搜索抖音（{len(KEYWORDS)} 个关键词）...")
    authors = {}
    for kw in KEYWORDS:
        print(f"  搜索: {kw}")
        items = douyin_search(kw)
        for item in items:
            if item.get('type') == 1 and item.get('aweme_info'):
                aweme = item['aweme_info']
                author = aweme.get('author', {})
                sec_uid = author.get('sec_uid', '')
                if not sec_uid:
                    continue
                stats = aweme.get('statistics', {})
                video = {
                    'desc': aweme.get('desc', '')[:80],
                    'digg_count': stats.get('digg_count', 0),
                    'comment_count': stats.get('comment_count', 0),
                }
                if sec_uid not in authors:
                    authors[sec_uid] = {
                        'nickname': author.get('nickname', ''),
                        'sec_uid': sec_uid, 'keyword': kw, 'videos': [],
                    }
                authors[sec_uid]['videos'].append(video)
        time.sleep(1.5)
    print(f"  搜索到 {len(authors)} 个账号")

    # 2. 获取详情 + 过滤
    print(f"\n[2/4] 获取详情并过滤...")
    token = feishu_token()
    existing = get_existing_names(token) if not clean else set()

    sorted_authors = sorted(
        authors.values(),
        key=lambda x: sum(v['digg_count'] for v in x['videos']),
        reverse=True,
    )

    kept = []
    for author_info in sorted_authors:
        sec_uid = author_info['sec_uid']
        nickname = author_info['nickname']

        # 跳过已存在的
        if nickname in existing:
            continue

        try:
            profile = douyin_user_profile(sec_uid)
            if not profile:
                continue

            follower_count = profile.get('follower_count', 0)
            signature = profile.get('signature', '')

            if follower_count > 5000000:
                continue
            if not is_ai_account(nickname, signature):
                continue

            top_videos = sorted(author_info['videos'], key=lambda x: x['digg_count'], reverse=True)
            kept.append({
                'nickname': nickname,
                'unique_id': str(profile.get('unique_id') or profile.get('short_id', '')),
                'follower_count': follower_count,
                'aweme_count': profile.get('aweme_count', 0),
                'total_favorited': profile.get('total_favorited', 0),
                'account_type': account_type(profile),
                'company': profile.get('enterprise_verify_reason', ''),
                'signature': signature[:100],
                'keyword': author_info['keyword'],
                'top_video_1_title': top_videos[0]['desc'] if len(top_videos) > 0 else '',
                'top_video_1_likes': top_videos[0]['digg_count'] if len(top_videos) > 0 else 0,
                'top_video_2_title': top_videos[1]['desc'] if len(top_videos) > 1 else '',
                'top_video_2_likes': top_videos[1]['digg_count'] if len(top_videos) > 1 else 0,
            })
            print(f"  KEEP [{len(kept)}] {nickname} (粉丝: {format_count(follower_count)})")
        except Exception as e:
            print(f"  ERROR {nickname}: {e}")
        time.sleep(1)

    if not kept:
        print("\n  没有新账号需要写入")
        return

    # 3. 清空旧数据（如果指定 --clean）
    if clean:
        print(f"\n[3/4] 清空旧数据...")
        records = feishu_get_records(token)
        ids = [r["record_id"] for r in records]
        if ids:
            feishu_delete_records(token, ids)
            print(f"  已清空 {len(ids)} 条")
    else:
        print(f"\n[3/4] 追加模式（保留旧数据）")

    # 4. 写入飞书
    print(f"\n[4/4] 写入飞书...")
    records = []
    for acc in kept:
        records.append({
            "账号名称": acc['nickname'],
            "抖音号": acc['unique_id'],
            "粉丝数": acc['follower_count'],
            "作品数": acc['aweme_count'],
            "总获赞": acc['total_favorited'],
            "账号类型": acc['account_type'],
            "所属公司": acc['company'],
            "内容方向": acc['signature'],
            "爆款视频1标题": acc['top_video_1_title'],
            "爆款视频1点赞": acc['top_video_1_likes'],
            "爆款视频2标题": acc['top_video_2_title'],
            "爆款视频2点赞": acc['top_video_2_likes'],
            "关注级别": "⚪ 待分析",
            "更新日期": TODAY,
        })

    for i in range(0, len(records), 10):
        batch = records[i:i+10]
        result = feishu_create_records(token, batch)
        if result.get('code') == 0:
            print(f"  写入 {len(batch)} 条")
        else:
            print(f"  写入失败: {result.get('msg', '')}")

    # 保存原始数据
    data_file = os.path.join(DATA_DIR, f"douyin_raw_data_{TODAY}.json")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(kept, f, ensure_ascii=False, indent=2)

    print(f"\n完成! 新增 {len(kept)} 个账号")
    print(f"  飞书表格: {FEISHU_URL}")
    print(f"  原始数据: {data_file}")


# ============================================================
# 命令: analyze - 分析指定账号
# ============================================================

def cmd_analyze(name):
    print("=" * 60)
    print(f"  分析账号: {name}")
    print("=" * 60)

    # 1. 从飞书找到这个账号
    token = feishu_token()
    records = feishu_get_records(token)

    target = None
    for item in records:
        fields = item.get("fields", {})
        n = fields.get("账号名称", "")
        if isinstance(n, list):
            n = n[0].get("text", "") if n else ""
        if n == name:
            target = item
            break

    # 2. 搜索抖音找到这个账号
    print(f"\n[1/3] 搜索抖音用户: {name}")
    items = douyin_search(name, count=10)
    sec_uid = None
    for item in items:
        if item.get('type') == 1 and item.get('aweme_info'):
            author = item['aweme_info'].get('author', {})
            if author.get('nickname', '') == name:
                sec_uid = author.get('sec_uid', '')
                break

    if not sec_uid:
        # 尝试模糊匹配
        for item in items:
            if item.get('type') == 1 and item.get('aweme_info'):
                author = item['aweme_info'].get('author', {})
                if name in author.get('nickname', ''):
                    sec_uid = author.get('sec_uid', '')
                    print(f"  模糊匹配到: {author.get('nickname')}")
                    break

    if not sec_uid:
        print(f"  未找到账号 {name}，请确认名称是否正确")
        return

    # 3. 获取用户详情
    print(f"\n[2/3] 获取用户详情...")
    profile = douyin_user_profile(sec_uid)
    if not profile:
        print("  获取失败")
        return

    print(f"\n  {'='*50}")
    print(f"  账号: {profile.get('nickname')}")
    print(f"  抖音号: {profile.get('unique_id') or profile.get('short_id')}")
    print(f"  粉丝: {format_count(profile.get('follower_count', 0))}")
    print(f"  关注: {profile.get('following_count', 0)}")
    print(f"  获赞: {format_count(profile.get('total_favorited', 0))}")
    print(f"  作品: {profile.get('aweme_count', 0)}")
    print(f"  类型: {account_type(profile)}")
    print(f"  认证: {profile.get('custom_verify', '') or profile.get('enterprise_verify_reason', '') or '无'}")
    print(f"  简介: {profile.get('signature', '')}")
    print(f"  {'='*50}")

    # 4. 获取视频列表
    print(f"\n[3/3] 获取视频列表...")
    time.sleep(1)
    videos = douyin_user_videos(sec_uid, count=50)
    print(f"  获取到 {len(videos)} 个视频\n")

    if not videos:
        print("  未获取到视频数据（可能需要更新Cookie）")
        return

    # 统计分析
    total_likes = 0
    total_comments = 0
    total_shares = 0
    video_data = []

    for v in videos:
        stats = v.get('statistics', {})
        likes = stats.get('digg_count', 0)
        comments = stats.get('comment_count', 0)
        shares = stats.get('share_count', 0)
        plays = stats.get('play_count', 0)
        desc = v.get('desc', '')[:80]
        create_time = v.get('create_time', 0)
        date_str = datetime.fromtimestamp(create_time).strftime('%Y-%m-%d') if create_time else ''

        total_likes += likes
        total_comments += comments
        total_shares += shares

        video_data.append({
            'desc': desc, 'likes': likes, 'comments': comments,
            'shares': shares, 'plays': plays, 'date': date_str,
        })

    # 按点赞排序
    video_data.sort(key=lambda x: x['likes'], reverse=True)

    avg_likes = total_likes // len(videos) if videos else 0
    avg_comments = total_comments // len(videos) if videos else 0

    print(f"  === 数据汇总 ===")
    print(f"  总点赞: {format_count(total_likes)} | 总评论: {format_count(total_comments)} | 总转发: {format_count(total_shares)}")
    print(f"  篇均点赞: {format_count(avg_likes)} | 篇均评论: {avg_comments}")
    print(f"  最早视频: {video_data[-1]['date'] if video_data else 'N/A'}")
    print(f"  最新视频: {video_data[0]['date'] if video_data else 'N/A'}")

    print(f"\n  === TOP 10 爆款视频 ===")
    for i, v in enumerate(video_data[:10]):
        print(f"  {i+1}. [{v['likes']:>6,}赞 {v['comments']:>4,}评 {v['shares']:>4,}转] {v['date']} {v['desc']}")

    print(f"\n  === 最近 5 个视频 ===")
    recent = sorted(video_data, key=lambda x: x['date'], reverse=True)[:5]
    for v in recent:
        print(f"  [{v['likes']:>6,}赞 {v['comments']:>4,}评] {v['date']} {v['desc']}")

    # 保存分析结果
    result = {
        'profile': {
            'nickname': profile.get('nickname'),
            'follower_count': profile.get('follower_count', 0),
            'total_favorited': profile.get('total_favorited', 0),
            'aweme_count': profile.get('aweme_count', 0),
            'signature': profile.get('signature', ''),
        },
        'stats': {
            'total_likes': total_likes, 'total_comments': total_comments,
            'total_shares': total_shares, 'avg_likes': avg_likes,
            'avg_comments': avg_comments,
        },
        'videos': video_data,
    }

    result_file = os.path.join(DATA_DIR, f"analyze_{name}_{TODAY}.json")
    with open(result_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n  分析结果已保存: {result_file}")


# ============================================================
# 命令: update - 更新所有账号的最新数据
# ============================================================

def cmd_update():
    print("=" * 60)
    print(f"  更新所有账号最新数据  [{TODAY}]")
    print("=" * 60)

    token = feishu_token()
    records = feishu_get_records(token)
    print(f"\n共 {len(records)} 条记录需要更新\n")

    # 先搜索获取 sec_uid 映射
    # 由于我们没有存 sec_uid，需要通过搜索名字来找
    updated = 0
    failed = []

    for item in records:
        fields = item.get("fields", {})
        name = fields.get("账号名称", "")
        if isinstance(name, list):
            name = name[0].get("text", "") if name else ""
        if not name:
            continue

        record_id = item["record_id"]

        try:
            # 搜索这个账号
            results = douyin_search(name, count=5)
            sec_uid = None
            for r in results:
                if r.get('type') == 1 and r.get('aweme_info'):
                    author = r['aweme_info'].get('author', {})
                    if name in author.get('nickname', ''):
                        sec_uid = author.get('sec_uid', '')
                        break

            if not sec_uid:
                failed.append(name)
                print(f"  SKIP {name} (未搜索到)")
                time.sleep(0.5)
                continue

            # 获取最新资料
            profile = douyin_user_profile(sec_uid)
            if not profile:
                failed.append(name)
                continue

            update_fields = {
                "粉丝数": profile.get('follower_count', 0),
                "作品数": profile.get('aweme_count', 0),
                "总获赞": profile.get('total_favorited', 0),
                "更新日期": TODAY,
            }
            result = feishu_update_record(token, record_id, update_fields)
            if result.get("code") == 0:
                updated += 1
                print(f"  [{updated}] {name} → 粉丝: {format_count(profile.get('follower_count', 0))}")
            else:
                failed.append(name)
                print(f"  FAIL {name}: {result.get('msg', '')}")

        except Exception as e:
            failed.append(name)
            print(f"  ERROR {name}: {e}")

        time.sleep(1.5)

    print(f"\n完成! 更新 {updated} 条, 失败 {len(failed)} 条")
    if failed:
        print(f"  失败账号: {', '.join(failed[:10])}")
    print(f"  飞书表格: {FEISHU_URL}")


# ============================================================
# 主入口
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("命令:")
        print("  collect [--clean]  搜索采集新账号")
        print("  analyze <账号名>   分析指定账号")
        print("  update             更新所有账号数据")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == 'collect':
        clean = '--clean' in sys.argv
        cmd_collect(clean=clean)
    elif cmd == 'analyze':
        if len(sys.argv) < 3:
            print("用法: python3 douyin_to_feishu.py analyze <账号名>")
            sys.exit(1)
        cmd_analyze(sys.argv[2])
    elif cmd == 'update':
        cmd_update()
    else:
        print(f"未知命令: {cmd}")
        print("可用命令: collect, analyze, update")
        sys.exit(1)


if __name__ == "__main__":
    main()
