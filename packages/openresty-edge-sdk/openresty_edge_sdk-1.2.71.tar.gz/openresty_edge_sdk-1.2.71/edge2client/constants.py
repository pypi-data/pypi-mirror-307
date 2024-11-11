# -*- coding: utf-8 -*-
from types import MappingProxyType

# Deprecated:
# To avoid affecting old interfaces, this constant is introduced to represent "delete/clear".
# It can continue to be used in old interfaces if needed.
# For new interfaces, please use DEFAULT instead
OFF = False
ON = True

waf_rule_sets_name2id = {
    'robots': 1,
    'generic': 2,
    'inject': 3,
    'trojans': 4,
    'xss': 5,
    'scanner_detection': 6,
    'protocol_enforcement': 7,
    'protocol_attack': 8,
    'application_attack_lfi': 9,
    'application_attack_rfi': 10,
    'application_attack_rce': 11,
    'application_attack_php': 12,
    'application_attack_nodejs': 13,
    'application_attack_xss': 14,
    'application_attack_sqli': 15,
    'application_attack_session_fixation': 16,
    'application_attack_java': 17,
}

valid_waf_thresholds = {
    'high': True,
    'medium': True,
    'low': True,
    'none': True,
}

cross_req_waf_threshold_scores = {
    'high': 1000,
    'medium': 100,
    'low': 10,
}

waf_threshold_scores = {
    'high': 12,
    'medium': 6,
    'low': 3,
}

ERROR_LOG_LEVELS = MappingProxyType({
    'stderr': 0,
    'emerg': 1,
    'alert': 2,
    'crit': 3,
    'error': 4,
    'warn': 5,
    'notice': 6,
    'info': 7,
    'debug': 8,
})


class Sentinel:
    """
    Sentinel is a singleton class that is used to indicate that a parameter is not provided.
    Sentinel: parameter is not provided
    None: parameter is provided and its value is None
    Any other value: parameter is provided and its value is not None
    """
    pass

DEFAULT = Sentinel()
