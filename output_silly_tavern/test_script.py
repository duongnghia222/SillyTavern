def extract_questions(file_path):
    questions = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('-'):
                question = line.lstrip('-').strip()
                questions.append(question)

    return questions

# Example usage
suggest_question_set = extract_questions("output_silly_tavern\Suggest_Question_Set.txt")
print("Extracted questions:")
for i, question in enumerate(suggest_question_set, 1):
    print(f"{i}. {question}")
