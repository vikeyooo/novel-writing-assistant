"""工具函数模块"""

def format_text(text: str, max_width: int = 80) -> str:
    """格式化文本"""
    lines = text.split('\n')
    formatted = []
    for line in lines:
        if len(line) > max_width:
            words = line.split()
            current_line = []
            for word in words:
                if len(' '.join(current_line + [word])) > max_width:
                    formatted.append(' '.join(current_line))
                    current_line = [word]
                else:
                    current_line.append(word)
            if current_line:
                formatted.append(' '.join(current_line))
        else:
            formatted.append(line)
    return '\n'.join(formatted)
