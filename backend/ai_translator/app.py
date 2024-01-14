from flask_cors import CORS
from flask import Flask, request, jsonify
from backend.ai_translator.translator.pdf_parser import PDFParser
from backend.ai_translator import OpenAIModel
from backend.ai_translator.translator import PDFTranslator

app = Flask(__name__)
CORS(app)


@app.route('/translate/pdf', methods=['POST'])
def translate():
    # 获取请求中的参数
    data = request.values

    pdf_file = request.files['file']
    # pdf_name = pdf_file.filename
    file_format = data.get('file_format')
    target_language = data.get('target_language')
    book = PDFParser().parse_pdf(pdf_file)
    # 实例化 PDFTranslator 类，并调用 translate_pdf() 方法

    translator = PDFTranslator(OpenAIModel)
    output_file_path = translator.translate_pdf(book, file_format, target_language)

    # 返回翻译结果
    response = {'code': 200, 'output_file_path': ''}
    if output_file_path is None:
        response['code'] = 500
    else:
        response['output_file_path'] = output_file_path.split("/")[-1]
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
