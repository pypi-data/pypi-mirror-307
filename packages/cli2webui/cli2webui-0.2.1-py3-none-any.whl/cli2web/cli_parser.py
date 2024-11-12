import subprocess
import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

@dataclass
class CommandOption:
    name: str
    long_name: Optional[str]
    description: str
    is_required: bool
    has_value: bool = True
    value_type: str = 'text'
    default_value: Optional[str] = None
    valid_values: Optional[List[str]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            'name': self.name,
            'long_name': self.long_name,
            'description': self.description,
            'is_required': self.is_required,
            'has_value': self.has_value,
            'value_type': self.value_type,
            'default_value': self.default_value,
            'valid_values': self.valid_values
        }

class CliParser:
    def __init__(self, command_name: str):
        self.command_name = command_name
        self.options: Dict[str, CommandOption] = {}

    def parse_help(self) -> List[CommandOption]:
        """解析命令的man手册"""
        try:
            # 使用 man 命令获取手册内容
            man_output = subprocess.check_output(
                f"man {self.command_name} | col -b",  # col -b 移除退格符等控制字符
                shell=True,
                text=True
            )
            
            # 提取选项部分
            options_section = self._extract_options_section(man_output)
            if options_section:
                self._parse_options(options_section)
            
            # 返回排序后的选项列表
            return sorted(self.options.values(), key=lambda x: x.name)
            
        except subprocess.CalledProcessError:
            # 如果获取man手册失败，尝试使用 --help
            return self._parse_help_fallback()

    def _extract_options_section(self, man_text: str) -> Optional[str]:
        """从man手册中提取选项部分"""
        # 查找选项部分的开始和结束
        sections = {
            'DESCRIPTION': [],  # 可能包含选项说明
            'OPTIONS': []       # 主要的选项部分
        }
        
        current_section = None
        for line in man_text.split('\n'):
            # 检测章节标题
            section_match = re.match(r'^([A-Z][A-Z\s]+)$', line.strip())
            if section_match:
                current_section = section_match.group(1)
                continue
            
            # 收集相关章节的内容
            if current_section in sections:
                sections[current_section].append(line)
        
        # 优先使用 OPTIONS 章节，如果没有则使用 DESCRIPTION
        options_text = '\n'.join(sections.get('OPTIONS', []))
        if not options_text:
            options_text = '\n'.join(sections.get('DESCRIPTION', []))
        
        return options_text

    def _parse_options(self, options_text: str) -> None:
        """解析选项部分"""
        current_option = None
        current_description = []
        
        # 选项的正则表达式模式
        option_pattern = (
            r'^\s*(?:'
            r'(-[a-zA-Z])(?:\[?=([A-Z][A-Z_]*)\]?)?'  # 短选项带可选或必需参数
            r'|'
            r'(--[a-zA-Z-]+)(?:\[?=([A-Z][A-Z_]*)\]?)?'  # 长选项带可选或必需参数
            r')'
            r'(?:\s+([A-Z][A-Z_]*))?\s*'  # 空格后的参数
            r'(.*)$'  # 描述部分
        )
        
        # 检查是否有参数关系说明
        has_arg_note = bool(re.search(
            r'Mandatory arguments to long options are mandatory for short options',
            options_text,
            re.IGNORECASE
        ))
        
        for line in options_text.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # 尝试匹配选项行
            option_match = re.match(option_pattern, line)
            
            if option_match:
                # 保存之前的选项
                if current_option:
                    self._add_option(
                        **current_option,
                        description='\n'.join(current_description).strip(),
                        has_arg_note=has_arg_note
                    )
                
                # 解析新选项
                short_opt, short_arg, long_opt, long_arg, space_arg, desc = option_match.groups()
                
                # 确定选项名称和参数信息
                name = short_opt or long_opt
                long_name = long_opt if short_opt else None
                
                # 确定参数需求
                has_value = False
                is_optional = True
                
                # 检查是否有参数
                if short_arg or long_arg or space_arg:
                    has_value = True
                    # 检查是否是可选参数（用方括号标记）
                    is_optional = '[' in line and ']' in line
                
                # 获取参数名称（用于确定参数类型）
                arg_name = short_arg or long_arg or space_arg
                
                current_option = {
                    'name': name,
                    'long_name': long_name,
                    'has_value': has_value,
                    'is_optional': is_optional,
                    'arg_name': arg_name
                }
                current_description = [desc] if desc else []
            
            # 继续收集选项描述
            elif current_option and line:
                current_description.append(line)
        
        # 保存最后一个选项
        if current_option:
            self._add_option(
                **current_option,
                description='\n'.join(current_description).strip(),
                has_arg_note=has_arg_note
            )

    def _add_option(self, name: str, long_name: Optional[str], description: str, 
                    has_value: bool = False, is_optional: bool = True,
                    arg_name: Optional[str] = None, has_arg_note: bool = False) -> None:
        """添加选项到选项字典"""
        if not name:
            return

        # 清理选项名称
        name = name.strip()
        if long_name:
            long_name = long_name.strip()

        # 确定参数类型
        value_type = 'text'  # 默认类型
        valid_values = None

        if has_value:
            # 根据参数名和描述确定类型
            if arg_name:
                if arg_name in ('NUM', 'NUMBER', 'COUNT', 'COLS', 'SIZE'):
                    value_type = 'number'
                elif arg_name in ('PATTERN', 'WORD', 'STRING'):
                    value_type = 'text'
                elif arg_name in ('WHEN', 'STYLE', 'FORMAT'):
                    value_type = 'select'
                    # 尝试从描述中提取有效值
                    values_match = re.search(
                        r'(?:can be|one of|可以是|其中之一)[：:]\s*[\'"]?(.*?)[\'"]?(?=[\.,]|\s*$|;)',
                        description
                    )
                    if values_match:
                        valid_values = [
                            v.strip(' \'"')
                            for v in re.split(r'[,，]\s*|\s+(?:or|或)\s+|\s+', values_match.group(1))
                            if v.strip()
                        ]

            # 从描述中确认类型
            if re.search(r'(?:number|integer|count|数字|整数)', description, re.IGNORECASE):
                value_type = 'number'
            elif re.search(r'(?:select|choose|specify|选择|指定).*?(?:from|between|从|在)', description, re.IGNORECASE):
                value_type = 'select'

        # 判断选项是否必需 - 选项本身永远是可选的
        is_required = False

        # 判断选项的参数是否必需（如果选项被使用）
        requires_arg = has_value and not is_optional

        # 创建或更新选项
        if name in self.options:
            existing_option = self.options[name]
            if description and description not in existing_option.description:
                existing_option.description = f"{existing_option.description}\n{description}".strip()
        else:
            option = CommandOption(
                name=name,
                long_name=long_name,
                description=description,
                is_required=is_required,  # 选项本身不是必需的
                has_value=has_value,
                value_type=value_type,
                valid_values=valid_values
            )
            # 如果选项需要参数，在描述中说明
            if requires_arg:
                option.description = f"{description}\n(当使用此选项时，必须提供参数)"
            # 如果有有效值列表，添加到描述中
            if valid_values:
                option.description = f"{option.description}\n可用值: {', '.join(valid_values)}"
            self.options[name] = option

    def _parse_help_fallback(self) -> List[CommandOption]:
        """当无法获取man手册时，使用--help作为后备方案"""
        try:
            help_output = subprocess.check_output(
                [self.command_name, '--help'],
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            self._parse_options(help_output)
            return sorted(self.options.values(), key=lambda x: x.name)
        except subprocess.CalledProcessError:
            return []