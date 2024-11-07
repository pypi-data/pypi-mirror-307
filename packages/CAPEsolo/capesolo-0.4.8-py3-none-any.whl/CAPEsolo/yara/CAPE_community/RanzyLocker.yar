rule RanzyLocker {
    meta:
        author = "ditekSHen"
        description = "Detects RanzyLocker ransomware"
        cape_type = "RanzyLocker Payload"
    strings:
        $hr1 = "776261646D696E2044454C4554452053595354454D53544154454241434B5550" ascii
        $hr2 = "776D69632E65786520534841444F57434F5059202F6E6F696E746572616374697665" ascii
        $hr3 = "626364656469742E657865202F736574207B64656661756C747D207265636F76657279656E61626C6564204E6F" ascii
        $hr4 = "776261646D696E2044454C4554452053595354454D53544154454241434B5550202D64656C6574654F6C64657374" ascii
        $hr5 = "626364656469742E657865202F736574207B64656661756C747D20626F6F74737461747573706F6C6963792069676E6F7265616C6C6661696C75726573" ascii
        $hr6 = "76737361646D696E2E6578652044656C65746520536861646F7773202F416C6C202F5175696574" ascii
        $hx1 = "476C6F62616C5C33353335354641352D303745392D343238422D423541352D314338384341423242343838" ascii
        $hx2 = "534F4654574152455C4D6963726F736F66745C45524944" ascii
        $hx3 = "227375626964223A22" ascii
        $hx4 = "226E6574776F726B223A22" ascii
        $hx5 = "726561646D652E747874" ascii
        $hx6 = "-nolan" fullword wide
        $o1 = { 8d 45 e9 89 9d 54 ff ff ff 88 9d 44 ff ff ff 3b }
        $o2 = { 8b 44 24 2? 8b ?c 24 34 40 8b 54 24 38 89 44 24 }
        $o3 = { 8b 44 24 2? 8b ?c 24 1c 89 44 24 34 8b 44 24 28 }
        $o4 = { 8b 44 24 2? 8b ?c 24 34 05 00 00 a0 00 89 44 24 }
    condition:
        uint16(0) == 0x5a4d and (all of ($hx*) or (2 of ($hr*) and 2 of ($hx*)) or (all of ($o*) and 2 of ($h*)))
}
