from fastapi import APIRouter

router = APIRouter()


@router.get("/tk_user_profile", include_in_schema=False)
async def tk_user_profile():
    from f2.apps.tiktok.handler import TiktokHandler

    kwargs = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "Referer": "https://www.tiktok.com/",
        },
        "proxies": {"http://": None, "https://": None},
        "cookie": "_ttp=2kGqYoVfg3DjUCEL6NQnx38hsCx; tt_chain_token=Po6z8SYovAXuRbmcuTJOOA==; delay_guest_mode_vid=5; passport_csrf_token=b72f49cc56d0fdb7d4e2a52ecbda85f9; passport_csrf_token_default=b72f49cc56d0fdb7d4e2a52ecbda85f9; tt_csrf_token=vMciH4UJ-EokvG_DUV2XD1gOZtzvAJey361M; perf_feed_cache={%22expireTimestamp%22:1746090000000%2C%22itemIds%22:[%227476565904256519470%22%2C%227488346066325261614%22%2C%227468473218769243423%22]}; s_v_web_id=verify_ma2gojvs_p7b9qUKB_USOI_4TSK_AhFo_Ynx2qCSEq1ue; multi_sids=7090315293859496966%3A38d942fdba8c5e20bb333d911ffae18f; cmpl_token=AgQQAPOqF-RO0rJbMpYcMR0__bBEgZiR_6nZYN-bwg; passport_auth_status=2ed59ea7a70c8cd41bc495458989e9ba%2C; passport_auth_status_ss=2ed59ea7a70c8cd41bc495458989e9ba%2C; uid_tt=887abb6db67fd02fda0e1f80be0d3fb026748d9f5759077ccf15404d29c2ef20; uid_tt_ss=887abb6db67fd02fda0e1f80be0d3fb026748d9f5759077ccf15404d29c2ef20; sid_tt=38d942fdba8c5e20bb333d911ffae18f; sessionid=38d942fdba8c5e20bb333d911ffae18f; sessionid_ss=38d942fdba8c5e20bb333d911ffae18f; store-idc=alisg; store-country-code=jp; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=c3aXGSWd5ezSdz2EAoyrEUAsZua8lBqi7rDoTjZLohYo6bO0Tj8NBpGtNxR-p9DJB3Hqwrge2NlncK1kSTHNRv2U2IHOLvN9K9D3UNz_bBOOqZ5lofrfEPBQtuvW0CMwkX3msB7UAHTP1lFTEVwAPRrAI7IePwQ-yPcH6_nsdd0VVfUck0i8zKFLdW__YUt5p-viCtTvqPRWnGev7_FnhBpSv-Iec6TtzgKxF3ZigvXf9pZIQFh5wWPTgVtdLVvAUtiqHLvX3WJ2JiULnHz_jAp4CqPbRRumFAecRJwxzUTHsnVQTib7nNjzNYyc6DCpou6wpitmNGD_LvW0xF9Qtr9TYJn9UvFDn0xpwbPNWgUN0gteQDLmPeVyg1ej4v9EeUCf8DXHFX1TEH6vQg9diMDkrbjfyj1s6kh4q7kHUCfDKd9punHgPdboLD7yn-ilir57ThEkiw1T492Eik12cPmM4SXRH4f35gU2B6qFTMUj5byipdSo-PiwTmsylACC; last_login_method=google; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; sid_guard=38d942fdba8c5e20bb333d911ffae18f%7C1745928430%7C15551979%7CSun%2C+26-Oct-2025+12%3A06%3A49+GMT; sid_ucp_v1=1.0.0-KGRmZjQzNzNjZjNjYTZhZDQ1NGRjMzJiZDg4OTlkNmYxN2Y0Zjc1OWEKGQiGiI-gmYb3smIQ7oHDwAYYsws4CEASSAQQAxoCbXkiIDM4ZDk0MmZkYmE4YzVlMjBiYjMzM2Q5MTFmZmFlMThm; ssid_ucp_v1=1.0.0-KGRmZjQzNzNjZjNjYTZhZDQ1NGRjMzJiZDg4OTlkNmYxN2Y0Zjc1OWEKGQiGiI-gmYb3smIQ7oHDwAYYsws4CEASSAQQAxoCbXkiIDM4ZDk0MmZkYmE4YzVlMjBiYjMzM2Q5MTFmZmFlMThm; odin_tt=4f33e00247bf71073194f85740a5e57e8af348a8528626f054a919ff91da00edbb4a144a03b26e41d30697211ec92d82f2a488994864152c9609513c89a895811d84ffcf9400f1417adba1e42228bf68; csrf_session_id=2529773b4e82245f378ab720d0f83f13; passport_fe_beating_status=true; ttwid=1%7CCAc5dMvTEXn2UgG6z-2zw7TyUpjeuqxFFmbWVs3NJIw%7C1745933042%7C3f69b7a2660e3242474eb245c7d79451b8d0190dfd5e035856eecf8d404eca3c; store-country-sign=MEIEDD0uUxd3YbqTtycgBgQgXdnJFNbcuMqmvGC4f5JAdAUVUayX_JjAHoSaWWIXjFwEEH9kGo5afU4FnhmH1MCfwlc; msToken=L3hhJg16B0BmGM7ITZot6rURy1St32lFS-fix93lRgUTAtN4XFSzQCWmoq6LPQC3-DfHl1LTAjwtiATHLU7kVMJZoZe4zGRbU3bosbtkcDdGpxUnOEoK2WH-NIqRGst0ngQzVaIDK-USsDh3gH7SS3Mphis=; msToken=8Gab0WRbM42LMt8oqSDm8JGZmSPbIku1YEoR-3WpKW1NhyqpZNQnVhPA6KQLLUXvx50K3CjOS-1C5Dgii9fpXXyx48Qq4kZnHEmFKDComvpThj3XsMW9GoygkMqVzV8V9psN5LFa3JzUC2Z7evrhGvMwayA=",
    }
    secUid = (
        "MS4wLjABAAAAQhcYf_TjRKUku-aF8oqngAfzrYksgGLRz8CKMciBFdfR54HQu3qGs-WoJ-KO7hO8"
    )
    uniqueId = "vantoan___"
    user = await TiktokHandler(kwargs).fetch_user_profile(secUid=secUid)
    # print("=================_to_raw================")
    # print(user._to_raw())
    user = await TiktokHandler(kwargs).fetch_user_profile(uniqueId=uniqueId)
    # print("=================_to_raw================")
    # print(user._to_raw())

    return user


@router.get("/tk_comment", include_in_schema=False)
async def tk_comment():
    from f2.apps.tiktok.handler import TiktokHandler

    kwargs = {
        "headers": {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
            "Referer": "https://www.tiktok.com/",
        },
        "proxies": {"http://": None, "https://": None},
        "cookie": "_ttp=2kGqYoVfg3DjUCEL6NQnx38hsCx; tt_chain_token=Po6z8SYovAXuRbmcuTJOOA==; delay_guest_mode_vid=5; passport_csrf_token=b72f49cc56d0fdb7d4e2a52ecbda85f9; passport_csrf_token_default=b72f49cc56d0fdb7d4e2a52ecbda85f9; tt_csrf_token=vMciH4UJ-EokvG_DUV2XD1gOZtzvAJey361M; perf_feed_cache={%22expireTimestamp%22:1746090000000%2C%22itemIds%22:[%227476565904256519470%22%2C%227488346066325261614%22%2C%227468473218769243423%22]}; s_v_web_id=verify_ma2gojvs_p7b9qUKB_USOI_4TSK_AhFo_Ynx2qCSEq1ue; multi_sids=7090315293859496966%3A38d942fdba8c5e20bb333d911ffae18f; cmpl_token=AgQQAPOqF-RO0rJbMpYcMR0__bBEgZiR_6nZYN-bwg; passport_auth_status=2ed59ea7a70c8cd41bc495458989e9ba%2C; passport_auth_status_ss=2ed59ea7a70c8cd41bc495458989e9ba%2C; uid_tt=887abb6db67fd02fda0e1f80be0d3fb026748d9f5759077ccf15404d29c2ef20; uid_tt_ss=887abb6db67fd02fda0e1f80be0d3fb026748d9f5759077ccf15404d29c2ef20; sid_tt=38d942fdba8c5e20bb333d911ffae18f; sessionid=38d942fdba8c5e20bb333d911ffae18f; sessionid_ss=38d942fdba8c5e20bb333d911ffae18f; store-idc=alisg; store-country-code=jp; store-country-code-src=uid; tt-target-idc=alisg; tt-target-idc-sign=c3aXGSWd5ezSdz2EAoyrEUAsZua8lBqi7rDoTjZLohYo6bO0Tj8NBpGtNxR-p9DJB3Hqwrge2NlncK1kSTHNRv2U2IHOLvN9K9D3UNz_bBOOqZ5lofrfEPBQtuvW0CMwkX3msB7UAHTP1lFTEVwAPRrAI7IePwQ-yPcH6_nsdd0VVfUck0i8zKFLdW__YUt5p-viCtTvqPRWnGev7_FnhBpSv-Iec6TtzgKxF3ZigvXf9pZIQFh5wWPTgVtdLVvAUtiqHLvX3WJ2JiULnHz_jAp4CqPbRRumFAecRJwxzUTHsnVQTib7nNjzNYyc6DCpou6wpitmNGD_LvW0xF9Qtr9TYJn9UvFDn0xpwbPNWgUN0gteQDLmPeVyg1ej4v9EeUCf8DXHFX1TEH6vQg9diMDkrbjfyj1s6kh4q7kHUCfDKd9punHgPdboLD7yn-ilir57ThEkiw1T492Eik12cPmM4SXRH4f35gU2B6qFTMUj5byipdSo-PiwTmsylACC; last_login_method=google; tiktok_webapp_theme_source=auto; tiktok_webapp_theme=dark; sid_guard=38d942fdba8c5e20bb333d911ffae18f%7C1745928430%7C15551979%7CSun%2C+26-Oct-2025+12%3A06%3A49+GMT; sid_ucp_v1=1.0.0-KGRmZjQzNzNjZjNjYTZhZDQ1NGRjMzJiZDg4OTlkNmYxN2Y0Zjc1OWEKGQiGiI-gmYb3smIQ7oHDwAYYsws4CEASSAQQAxoCbXkiIDM4ZDk0MmZkYmE4YzVlMjBiYjMzM2Q5MTFmZmFlMThm; ssid_ucp_v1=1.0.0-KGRmZjQzNzNjZjNjYTZhZDQ1NGRjMzJiZDg4OTlkNmYxN2Y0Zjc1OWEKGQiGiI-gmYb3smIQ7oHDwAYYsws4CEASSAQQAxoCbXkiIDM4ZDk0MmZkYmE4YzVlMjBiYjMzM2Q5MTFmZmFlMThm; odin_tt=4f33e00247bf71073194f85740a5e57e8af348a8528626f054a919ff91da00edbb4a144a03b26e41d30697211ec92d82f2a488994864152c9609513c89a895811d84ffcf9400f1417adba1e42228bf68; csrf_session_id=2529773b4e82245f378ab720d0f83f13; passport_fe_beating_status=true; ttwid=1%7CCAc5dMvTEXn2UgG6z-2zw7TyUpjeuqxFFmbWVs3NJIw%7C1745933042%7C3f69b7a2660e3242474eb245c7d79451b8d0190dfd5e035856eecf8d404eca3c; store-country-sign=MEIEDD0uUxd3YbqTtycgBgQgXdnJFNbcuMqmvGC4f5JAdAUVUayX_JjAHoSaWWIXjFwEEH9kGo5afU4FnhmH1MCfwlc; msToken=L3hhJg16B0BmGM7ITZot6rURy1St32lFS-fix93lRgUTAtN4XFSzQCWmoq6LPQC3-DfHl1LTAjwtiATHLU7kVMJZoZe4zGRbU3bosbtkcDdGpxUnOEoK2WH-NIqRGst0ngQzVaIDK-USsDh3gH7SS3Mphis=; msToken=8Gab0WRbM42LMt8oqSDm8JGZmSPbIku1YEoR-3WpKW1NhyqpZNQnVhPA6KQLLUXvx50K3CjOS-1C5Dgii9fpXXyx48Qq4kZnHEmFKDComvpThj3XsMW9GoygkMqVzV8V9psN5LFa3JzUC2Z7evrhGvMwayA=",
    }
    secUid = (
        "MS4wLjABAAAAQhcYf_TjRKUku-aF8oqngAfzrYksgGLRz8CKMciBFdfR54HQu3qGs-WoJ-KO7hO8"
    )
    uniqueId = "vantoan___"
    user = await TiktokHandler(kwargs).fetch_user_profile(secUid=secUid)
    # print("=================_to_raw================")
    # print(user._to_raw())
    user = await TiktokHandler(kwargs).fetch_user_profile(uniqueId=uniqueId)
    # print("=================_to_raw================")
    # print(user._to_raw())

    return user
