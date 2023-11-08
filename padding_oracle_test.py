from padding_oracle.exploit_oracle import oracle_solver
from padding_oracle.crypto_util import encrypt, decrypt, pad, unpad
import os
import random

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 3874
    iv = b'a1b2c3d4e5f6g7h8'
    padded_pt = pad(b'djbernstein')
    ct = encrypt(iv, padded_pt)
    print(ct)
    print(padded_pt)
    #print(oracle_solver(host, port, iv, ct))


    #statistical test
    for i in range(10):
        iv = os.urandom(16)
        pt = pad(os.urandom(random.randint(0,15)))
        ct = encrypt(iv, pt)
        if pt != oracle_solver(host,port,iv,ct):
            print(f"error on input: iv {iv}, pt {pt}, ct {ct}")
    #tests for edge case where there are two possible results, given this iv and ct \x02\x02 is the first hit
    iv = 16*b'\x00'
    pt = pad(b"ptendingon0x02\x02")
    ct = encrypt(iv,pt)
    assert pt == oracle_solver(host, port, iv, ct)
    
    '''
    host = "141.72.5.194"
    port = 18732
    plain2_3_1 = b''
    iv = 0x0478eabe443992c0b2b53cfc50aea04a.to_bytes(16, byteorder='big')
    ct = 0x566b0c7206dbb19efa9b296696af2652.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0x566b0c7206dbb19efa9b296696af2652.to_bytes(16, byteorder='big')
    ct = 0xd6900e8af1c80b3c79a3888f26bc3f18.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0xd6900e8af1c80b3c79a3888f26bc3f18.to_bytes(16, byteorder='big')
    ct = 0x7153ee46bef72e70ec07c5d0ccde2c4f.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0x7153ee46bef72e70ec07c5d0ccde2c4f.to_bytes(16, byteorder='big')
    ct = 0x724bfe8c2e82458bf0c329f0a1393770.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0x724bfe8c2e82458bf0c329f0a1393770.to_bytes(16, byteorder='big')
    ct = 0x50d21f2a3a7859d34cdb516750c4d1db.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0x50d21f2a3a7859d34cdb516750c4d1db.to_bytes(16, byteorder='big')
    ct = 0x9ce58f9872d87a31f6b0ba2f2ad5954f.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    iv = 0x9ce58f9872d87a31f6b0ba2f2ad5954f.to_bytes(16, byteorder='big')
    ct = 0x8334bb512ae7507b52e501b2e86ced6b.to_bytes(16, byteorder='big')
    plain2_3_1 += oracle_solver(host, port, iv, ct)
    print(plain2_3_1)
    plain2_3_2 = b''
    iv = 0x4fd219786fc926b14ac605b939196546.to_bytes(16, byteorder='big')
    ct = 0x3783a3acdea669ebc2a25faac92de5d2.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x3783a3acdea669ebc2a25faac92de5d2.to_bytes(16, byteorder='big')
    ct = 0x4f1b61d80c1110007855dbdb447278e6.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x4f1b61d80c1110007855dbdb447278e6.to_bytes(16, byteorder='big')
    ct = 0x00a15dedf2291da7a7ac98e90ded950e.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x00a15dedf2291da7a7ac98e90ded950e.to_bytes(16, byteorder='big')
    ct = 0x23b81e6d9ddce5399b733956fd83986d.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x23b81e6d9ddce5399b733956fd83986d.to_bytes(16, byteorder='big')
    ct = 0x21821fe00f4833eef95a7ab323e8bece.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x21821fe00f4833eef95a7ab323e8bece.to_bytes(16, byteorder='big')
    ct = 0xa920642291948c6bc5c14511bf3dda1f.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0xa920642291948c6bc5c14511bf3dda1f.to_bytes(16, byteorder='big')
    ct = 0xa4f53424254f4e33a7097539b92d8612.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0xa4f53424254f4e33a7097539b92d8612.to_bytes(16, byteorder='big')
    ct = 0x110aa72629e43ed763ab866dfaade621.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x110aa72629e43ed763ab866dfaade621.to_bytes(16, byteorder='big')
    ct = 0x5cd895adc6a703bd2dc1627d7c51f0f2.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x5cd895adc6a703bd2dc1627d7c51f0f2.to_bytes(16, byteorder='big')
    ct = 0x6240633bf1cf5f8ba0d136f6f66e4163.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x6240633bf1cf5f8ba0d136f6f66e4163.to_bytes(16, byteorder='big')
    ct = 0x8879081e1f4879810ae83ab01890de03.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x8879081e1f4879810ae83ab01890de03.to_bytes(16, byteorder='big')
    ct = 0x6de960ffce2e89731d576044817dfef3.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    iv = 0x6de960ffce2e89731d576044817dfef3.to_bytes(16, byteorder='big')
    ct = 0x64827a5485b0778492e7f524e42860aa.to_bytes(16, byteorder='big')
    plain2_3_2 += oracle_solver(host, port, iv, ct)
    print(plain2_3_2)
    

    plain2_3_3 = b''
    iv = 0x6335b5933b0fe17eb023457e1dbb6244.to_bytes(16, byteorder='big')
    ct = 0x8cc405bb829297f8e98e113dea8792f5.to_bytes(16, byteorder='big')
    plain2_3_3 += oracle_solver(host, port, iv, ct)
    iv = 0x8cc405bb829297f8e98e113dea8792f5.to_bytes(16, byteorder='big')
    ct = 0x3e416f023a38da02cfebabac13e2669a.to_bytes(16, byteorder='big')
    plain2_3_3 += oracle_solver(host, port, iv, ct)
    iv = 0x3e416f023a38da02cfebabac13e2669a.to_bytes(16, byteorder='big')
    ct = 0xaa2248b3890eb356532e64c39d2c4938.to_bytes(16, byteorder='big')
    plain2_3_3 += oracle_solver(host, port, iv, ct)
    iv = 0xaa2248b3890eb356532e64c39d2c4938.to_bytes(16, byteorder='big')
    ct = 0xb5a425ce4809f0476f47b30d0e9fdf9a.to_bytes(16, byteorder='big')
    plain2_3_3 += oracle_solver(host, port, iv, ct)
    iv = 0xb5a425ce4809f0476f47b30d0e9fdf9a.to_bytes(16, byteorder='big')
    ct = 0xc8dc6af091cc534f5ea0049d3ebd63db.to_bytes(16, byteorder='big')
    plain2_3_3 += oracle_solver(host, port, iv, ct)
    print(plain2_3_3)
    '''
    #b'Emerson Brady Von Terra nach Sol Emerson Brady Von Terra nach Sol Der erste Mensch auf der Sonne.\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f\x0f'
    #b'Ein Programmierer aus Mannheim, recht schlau, verzweifelte, denn sein Code war im Bau. Mit einer Tasse Kaffee in der Hand, sah er den Code, der nicht stand, und rief: "Oh Code, sei mir gn\xc3\xa4dig, genau!"\x07\x07\x07\x07\x07\x07\x07'
    #b'https://web.archive.org/web/20140207013940/http://www.kryptochef.net/\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'
    #To-DO: Update Parser, test for \x02\x02 edge case, test random input, documentation, solve bauers things