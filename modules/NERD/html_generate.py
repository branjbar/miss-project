"""
Here we construct some html pages for offline study of extracted names from text, etc
"""
__author__ = 'Bijan'


def initialize_html():
    """
    constructs the body of html
    """
    html_code = """
                <!DOCTYPE html>
                <html>
                <body>

                <h1>MiSS Sample Export Page</h1>

                <h4> Each notarial act is first preprocessed to remove extra space and odd symbols.
                Then Using the Meertens Institute data, names are highlighted as
                <span style="background-color: #FF88FF"> Female First Name </span>,
                <span style="background-color: #00FFFF"> Male First Name </span> and
                <span style="background-color: #FFFF00"> Last Name</span>.
                </h4>
                <hr>
            """
    return html_code


def save_html(html_code, file_name="sample_html.html"):
    """
    stores the html_code in file_name.
    """

    # close the html_code with final tage
    html_code += """
                        </body>
                    </html>
                """

    # store html_code in file
    text_file = open(file_name, "w")
    text_file.write(html_code)
    text_file.close()


def highlight_text(index, text, index_dict):
    html_code = "<p> #" + str(index) + ')  '

    for index, word in enumerate(text.split()):
        if index_dict.get(index):
            if index_dict.get(index) == "last_name":
                html_code += """ <span style="background-color: #FFFF00"> """ + word + """</span> """
            if index_dict.get(index) == "first_name_m":
                html_code += """ <span style="background-color: #00FFFF"> """ + word + """</span> """
            if index_dict.get(index) == "first_name_f":
                html_code += """ <span style="background-color: #FF88FF"> """ + word + """</span> """

        else:
            html_code += word + ' '
    html_code += "</p> \n"

    return html_code


def export_html(text_list):
    """
        text_list is a list of [text, text_index]
    """
    html_code = initialize_html()

    for index, text in enumerate(text_list):
        html_code += highlight_text(index, text[0], text[1])

    save_html(html_code)


def main():
    html_code = initialize_html()
    html_code += highlight_text('Bijan is a nice guy', [1,3])
    save_html(html_code)


if __name__ == "__main__":
    main()