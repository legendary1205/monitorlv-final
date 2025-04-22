# placeholder for SNMP code
# utils/snmp.py

from pysnmp.hlapi import *

def get_snmp_value(ip, community, oid):
    """دریافت مقدار OID خاص از طریق SNMP"""
    try:
        iterator = getCmd(
            SnmpEngine(),
            CommunityData(community, mpModel=1),  # SNMP v2c
            UdpTransportTarget((ip, 161), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )

        errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

        if errorIndication:
            return None
        elif errorStatus:
            return None
        else:
            for varBind in varBinds:
                return int(varBind[1])
    except Exception:
        return None

def get_bandwidth_usage(ip, community="public", iface_index=2):
    """
    خواندن حجم دریافتی (rx) و ارسالی (tx) از کارت شبکه
    iface_index: شماره کارت شبکه (مثلاً 2 برای eth0)
    """
    in_oid = f"1.3.6.1.2.1.2.2.1.10.{iface_index}"   # ifInOctets
    out_oid = f"1.3.6.1.2.1.2.2.1.16.{iface_index}"  # ifOutOctets

    in_bytes = get_snmp_value(ip, community, in_oid)
    out_bytes = get_snmp_value(ip, community, out_oid)

    if in_bytes is None or out_bytes is None:
        return None

    return {
        "rx_mb": round(in_bytes / 1024 / 1024, 2),
        "tx_mb": round(out_bytes / 1024 / 1024, 2)
    }
