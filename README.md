# 🚀 MSFVenom Payload Generator

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Metasploit](https://img.shields.io/badge/Metasploit-Framework-red)](https://www.metasploit.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-alex--chh-blue)](https://github.com/alex-chh)

**高級 Metasploit Payload 生成工具** - 專為滲透測試人員和安全研究人員設計的互動式命令行工具，提供完整的 payload 生成和 listener 配置自動化功能。

## ✨ 功能特色

### 🎯 智能 Payload 生成
- ✅ **30+ 種 payload 類型**支援（Meterpreter、Shell、Stageless）
- ✅ **跨平台支援**: Windows、Linux、Android、macOS、PHP、Python、Java
- ✅ **多重架構**: x86、x64 完整支援
- ✅ **智能分組顯示**: 按類別分類，方便選擇

### 🔒 高級編碼技術
- ✅ **30+ 種編碼器**: Shikata Ga Nai、Alpha Mixed、XOR 等
- ✅ **多重編碼技術**: 支援 encoder chaining
- ✅ **可調迭代次數**: 1-∞ 次編碼迭代
- ✅ **編碼器分類系統**: 按架構和類型智能分組

### 🌐 遠端執行能力
- ✅ **SSH 遠端連線**: 直接在 Kali server 執行 msfvenom
- ✅ **自動 SCP 下載**: 生成後自動下載 payload 檔案
- ✅ **雙模式執行**: 本地/遠端執行無縫切換
- ✅ **連接驗證**: 自動檢測 SSH 連接狀態

### 📋 自動化配置
- ✅ **自動 Listener 配置**: 生成 Metasploit RC 檔案
- ✅ **完整 handler 設置**: 多重 session 管理配置
- ✅ **一鍵啟動命令**: 提供直接執行指令
- ✅ **配置摘要顯示**: 生成前確認所有參數

## 🛠 技術架構

```python
# 核心類別結構
MSFPayloadGenerator
├── check_msfvenom()          # 環境檢測與驗證
├── get_user_input()          # 互動式配置收集
├── generate_payload()        # Payload 生成引擎
├── generate_listener_config() # Listener 配置生成
└── run()                     # 主執行流程控制
```

## 📦 安裝與使用

### 環境要求
- Python 3.8+
- Metasploit Framework (msfvenom)
- SSH 客戶端 (可選，用於遠端執行)

### 快速開始
```bash
# 克隆專案
git clone https://github.com/alex-chh/msf-payload-generator.git
cd msf-payload-generator

# 執行工具
python msf_payload_generator.py
```

### 使用範例
```bash
# 本地生成 Windows Meterpreter payload
? 選擇平台: windows
? 選擇架構: x64  
? 選擇 Payload: meterpreter/reverse_tcp
? LHOST: 192.168.1.100
? LPORT: 4444
? 輸出格式: exe
? 編碼器: x86/shikata_ga_nai (迭代3次)

# 自動生成 listener.rc 並提供啟動命令
msfconsole -r listener.rc
```

## 🎯 支援的 Payload 類型

### Meterpreter Payloads
- `meterpreter/reverse_tcp` - 標準反向連接
- `meterpreter/reverse_http` - HTTP 協議傳輸
- `meterpreter/reverse_https` - HTTPS 加密傳輸
- `meterpreter/reverse_tcp_ssl` - SSL 加密連接
- `meterpreter/reverse_winhttp` - Windows HTTP
- `meterpreter/reverse_winhttps` - Windows HTTPS

### Shell Payloads
- `shell/reverse_tcp` - 標準反向 Shell
- `shell/bind_tcp` - 綁定式 Shell
- `shell/reverse_http` - HTTP Shell
- `shell/reverse_https` - HTTPS Shell

### Stageless Payloads
- `meterpreter_reverse_tcp` - 無階段 Meterpreter
- `meterpreter_reverse_http` - 無階段 HTTP
- `meterpreter_reverse_https` - 無階段 HTTPS

### 平台特定 Payloads
- **Windows**: x86/x64 Meterpreter/Shell
- **Linux**: x86/x64 Meterpreter/Shell  
- **Android**: Meterpreter HTTP/HTTPS
- **Web**: PHP/Python/Java Payloads

## 🔧 編碼器系統

### x86 編碼器
- `x86/shikata_ga_nai` - 多態編碼（經典）
- `x86/alpha_mixed` - 字母混合編碼
- `x86/alpha_upper` - 大寫字母編碼
- `x86/xor` - XOR 編碼
- `x86/unicode_mixed` - Unicode 混合

### x64 編碼器  
- `x64/xor` - 64位 XOR 編碼
- `x64/xor_dynamic` - 動態 XOR
- `x64/zutto_dekiru` - 日語編碼器

### 多重編碼組合
- `x86/shikata_ga_nai + x86/alpha_upper`
- `x86/shikata_ga_nai + x86/xor`
- `x86/shikata_ga_nai + x64/xor`

## 🌐 遠端執行模式

### SSH 連接配置
```bash
# 自動偵測遠端 Kali 環境
? SSH 主機: 192.168.1.200
? SSH 用戶: kali
? 密碼/金鑰: [自動驗證]

# 在遠端執行 msfvenom 並下載結果
✅ 遠端執行成功
✅ Payload 下載完成: payload.exe
```

### 優勢特性
- 🔒 **安全傳輸**: 使用 SSH 加密通道
- ⚡ **效能優化**: 遠端執行節省本地資源
- 🔄 **自動重試**: 網絡異常自動重連
- 📊 **進度顯示**: 即時顯示執行狀態

## 📊 輸出格式支援

| 平台 | 支援格式 | 說明 |
|------|----------|------|
| Windows | exe, dll, psh | 可執行檔、DLL、PowerShell |
| Linux | elf, so | ELF 可執行檔、共享庫 |
| Android | apk | Android 應用包 |
| Web | php, py | PHP/Python 腳本 |
| macOS | macho | Mach-O 可執行檔 |

## 🚀 進階功能

### 自動化整合
```python
# 程式化調用示例
from msf_payload_generator import MSFPayloadGenerator

generator = MSFPayloadGenerator()
generator.payload_config = {
    'platform': 'windows',
    'arch': 'x64',
    'payload_type': 'meterpreter/reverse_tcp',
    'lhost': '192.168.1.100',
    'lport': '4444',
    'encoder': 'x86/shikata_ga_nai',
    'iterations': 3
}

generator.generate_payload()
generator.generate_listener_config()
```

### 批量處理
支援通過配置文件批量生成多個 payload，適合紅隊行動中的多目標攻擊。

### 日誌記錄
完整的執行日誌記錄，便於審計和故障排除。

## 🧩 相容性指南

### 平台前綴的 Payload 規則
- 當選擇的 `payload_type` 已包含平台前綴（例如 `windows/x64/meterpreter/reverse_https`、`linux/x64/shell/reverse_tcp`），生成命令會直接使用該值，不會再拼接 `platform/arch`，避免出現 `windows/x64/windows/...` 的錯誤。
- 對應程式位置：`msf_payload_generator.py:302`、`msf_payload_generator.py:387`。

### 編碼器相容性準則
- 目標架構為 `x86` 時：優先使用 `x86/*` 編碼器；`x64/*` 與其他架構編碼器（`ppc/`、`sparc/`、`mips*`）視為不相容。
- 目標架構為 `x64` 時：優先使用 `x64/*` 編碼器；`x86/*` 與其他架構編碼器視為不相容。
- 通用編碼器（`generic/*`、`cmd/*`、`php/*`）視為跨架構可用。
- 多重編碼（`a + b`）需各編碼器皆相容才視為相容；否則會提示並允許改選。
- 對應程式位置：`msf_payload_generator.py:208-221`（判斷）、`msf_payload_generator.py:223-279`（推薦與回退）。

### 推薦分組與回退行為
- 在編碼器選擇流程中，會先列出「推薦（相容於目標架構）」分組，其後再列出其他分組，空分組顯示 `(無)`。
- 若選到不相容編碼器，系統會提示並提供從「推薦」清單改選的選項；若沒有相容選項則回退為不使用編碼器繼續流程。

### 常見錯誤與修正
- 錯誤：`Error: invalid payload: windows/x64/windows/meterpreter/reverse_https`
  - 原因：同時選了平台前綴型 payload，且程式又拼接了 `platform/arch`。
  - 修正：自動檢測平台前綴並直接使用；已在生成命令與 listener 設定同步修正。
  - 對應程式位置：`msf_payload_generator.py:302-310`、`msf_payload_generator.py:387-397`。

## 🔒 安全最佳實踐

### 輸入驗證
- ✅ 所有用戶輸入均經過驗證和過濾
- ✅ 防止命令注入攻擊
- ✅ 路徑遍歷保護

### 執行安全
- ✅ 超時控制防止無限執行
- ✅ 資源使用限制
- ✅ 錯誤處理和日誌記錄

### 傳輸安全
- ✅ SSH 加密傳輸
- ✅ 檔案權限管理
- ✅ 敏感信息保護

## 📈 效能表現

### 生成速度
| Payload 類型 | 本地執行 | 遠端執行 |
|-------------|---------|---------|
| Windows exe | ~2-3秒 | ~5-8秒 |
| Linux elf | ~1-2秒 | ~3-5秒 |
| Android apk | ~10-15秒 | ~15-25秒 |

### 資源使用
- 記憶體佔用: < 50MB
- CPU 使用率: < 5%
- 網絡帶寬: 最小化傳輸

## 🛠 開發與貢獻

### 專案結構
```
msf-payload-generator/
├── msf_payload_generator.py  # 主程式
├── requirements.txt          # 依賴套件
├── README.md                 # 說明文件
├── examples/                 # 使用範例
│   ├── windows_payload.exe
│   └── listener.rc
├── tests/                    # 測試用例
│   ├── test_generator.py
│   └── test_configs.py
└── docs/                     # 技術文檔
    ├── payload_types.md
    └── encoders_guide.md
```

### 開發指南
1. Fork 本專案
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 測試
```bash
# 運行單元測試
python -m pytest tests/

# 運行整合測試  
python tests/integration_test.py
```

## 📝 版本歷史

### v1.0.0 (2024-12-08)
- ✅ 初始版本發布
- ✅ 基礎 payload 生成功能
- ✅ 互動式命令行界面
- ✅ Listener 配置自動生成
- ✅ 遠端執行支援

## 🤝 貢獻者

- **Alex Chen** - [alex-chh](https://github.com/alex-chh) - 專案創建者和維護者

歡迎提交 Issue 和 Pull Request！

## 📜 許可證

本專案採用 MIT 許可證 - 詳見 [LICENSE](LICENSE) 文件。

## 🙏 致謝

- **Metasploit Framework** 團隊提供強大的滲透測試工具
- **Python 社區** 提供優秀的開發生態
- **安全研究社區** 的持續貢獻和反饋

## 🔗 相關專案

- [pentest-automation-framework-2025](https://github.com/alex-chh/pentest-automation-framework-2025) - 滲透測試自動化框架
- [sliver-c2-dropper](https://github.com/alex-chh/sliver-c2-dropper) - Sliver C2 Agent Dropper
- [vba-red-team-testing-framework](https://github.com/alex-chh/vba-red-team-testing-framework) - VBA 紅隊測試框架

## 📞 支持與反饋

如果您遇到任何問題或有建議，請通過以下方式聯繫：

- 🐛 [提交 Issue](https://github.com/alex-chh/msf-payload-generator/issues)
- 💬 [討論區](https://github.com/alex-chh/msf-payload-generator/discussions)
- 📧 郵件: [專案維護者](mailto:)

---

**⭐ 如果這個專案對您有幫助，請給它一個 Star！**

[![Star History Chart](https://api.star-history.com/svg?repos=alex-chh/msf-payload-generator&type=Date)](https://star-history.com/#alex-chh/msf-payload-generator&Date)
