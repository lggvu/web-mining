prompt_template = '''You are a helpful virtual advisor named Lily. You can help customers answer questions about laptops. Your final goal is to help customer buy a suitable laptop.
If you cannot decide a final product, feel free to ask follow up questions to narrow down the search.
If the user decide to end the conversation, ask for their personal information to help them connect to a salesperson.
The answer is given in Vietnamese. Always answer in Vietnamese language.

You can use the following information to answer the question at the end:
### Information: 
{context}

### Question: {question}
'''

# -*- encoding: utf-8 -*-

def format_dict_to_string(data):
    result_strings = []
    for item in data:
        question = item['source']['question']
        answer = item['source']['answer']
        
        formatted_string = f"question: {question}\nanswer: {answer}\n"
        result_strings.append(formatted_string)
    
    return result_strings

def transform(input):
    try:
        to_string = format_dict_to_string(input)
        result = "\n".join(to_string)
    except Exception as e:
        print("Error: ", e) 
        print("Warning: Context not found, either the database is not bulked yet or the request could not be successful!")
        result = ""

    return result

if __name__ == "__main__":
    reponse = [{'score': 6.2138734, 'source': {'answer': 'Laptop Lenovo Ideapad 5 Pro 14IAP7 i5 1240P (82SH000SVN) có thiết kế vỏ kim loại đẹp mắt, màu xám, khối lượng chỉ 1.42 kg, thuận tiện mang theo di động.', 'question': 'Laptop Lenovo Ideapad 5 Pro 14IAP7 i5 1240P (82SH000SVN) có thiết kế như thế nào, và khối lượng của máy là bao nhiêu?'}}, {'score': 6.2103353, 'source': {'answer': 'Màn hình 15.6 inch của Laptop Lenovo Ideapad 3 có độ phân giải Full HD (1920 x 1080), công nghệ chống chói Anti Glare giúp giảm ánh sáng phản chiếu.', 'question': 'Màn hình của Laptop Lenovo Ideapad 3 có độ phân giải và kích thước như thế nào, cùng với công nghệ chống chói là gì?'}}, {'score': 5.9273424, 'source': {'answer': 'Laptop Lenovo Ideapad 3 15IAU7 i5 (82RK001PVN) có thiết kế đẹp mắt với vỏ nhựa sơn màu xám, nặng 1.63 kg, thuận tiện để mang theo di động và sử dụng ở nhiều nơi.', 'question': 'Laptop Lenovo Ideapad 3 15IAU7 i5 (82RK001PVN) có thiết kế như thế nào, và liệu khối lượng 1.63 kg có thuận tiện mang theo không?'}}]
    print(transform(reponse))