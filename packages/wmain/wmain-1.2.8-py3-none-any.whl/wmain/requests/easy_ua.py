from random import choice

platforms = {
    "Windows": [
        "Windows NT 10.0",
        "Windows NT 6.3",
        "Windows NT 6.2",
        "Windows NT 6.1",
        "Windows NT 6.0",
        "Windows NT 5.1",
        "Windows NT 5.0",
    ],
    "Mac": [
        "Macintosh; Intel Mac OS X 10_14_6",
        "Macintosh; Intel Mac OS X 10_13_6",
        "Macintosh; Intel Mac OS X 10_12_6",
        "Macintosh; Intel Mac OS X 10_11_6",
        "Macintosh; Intel Mac OS X 10_10_5",
    ],
    "iOS": [
        "iPad; CPU OS 13_3 like Mac OS X",
        "iPad; CPU OS 12_4_4 like Mac OS X",
        "iPhone; CPU iPhone OS 13_3 like Mac OS X",
        "iPhone; CPU iPhone OS 12_4_4 like Mac OS X",
    ],
    "Android": [
        "Linux; Android 9.0; SM-G965F Build/PPR1.180610.011",
        "Linux; Android 8.0.0; SM-G950F Build/R16NW",
        "Linux; Android 7.0; SAMSUNG SM-G930F Build/NRD90M",
        "Linux; Android 6.0.1; SAMSUNG SM-G920F Build/MMB29K",
    ],
}

browsers = [
    "Chrome/80.0.3987.149",
    "Firefox/74.0",
    "Safari/537.36",
    "Edge/18.17763",
    "Opera/66.0.3515.115",
]


def __get_ua(version, browser):
    return f"Mozilla/5.0 ({version}) {browser}"


def get_random(platform=None):
    if isinstance(platform, str):
        platform = platform.lower()
        if platform in ["windows", "win"]:
            platform = "Windows"
        elif platform in ["mac", "macos"]:
            platform = "Mac"
        elif platform in ["ios", "iphone", "ipad"]:
            platform = "iOS"
        elif platform in ["android", "google"]:
            platform = "Android"
    if platform in platforms:
        return __get_ua(choice(platforms[platform]), choice(browsers))
    return __get_ua(choice(sum(platforms.values(), [])), choice(browsers))


def get_random_windows_ua():
    return get_random("Windows")


def get_random_mac_ua():
    return get_random("Mac")


def get_random_ios_ua():
    return get_random("iOS")


def get_random_android_ua():
    return get_random("Android")
