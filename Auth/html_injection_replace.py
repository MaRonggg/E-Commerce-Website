
def replace_dangerous_characters(html_bytes:bytes):
    # suppose I get the bytes of body
    # and I will replace character within it to be what I want
    # replace & to &amp;
    html_bytes = html_bytes.replace(b'&', b'&amp;')
    # replace < to &lt;
    html_bytes = html_bytes.replace(b'<', b'&lt;')
    # replace > to &gt;
    html_bytes = html_bytes.replace(b'>', b'&gt;')

    return html_bytes

def escape_html_chars(message: str):
    # suppose I get the bytes of body
    # and I will replace character within it to be what I want
    # replace & to &amp;
    message = message.replace('&', '&amp;')
    # replace < to &lt;
    message = message.replace('<', '&lt;')
    # replace > to &gt;
    message = message.replace('>', '&gt;')

    return message


