from neat import Neat

neat = Neat()

@neat.lm(stream=True)
def generate_text():
    return [
        neat.system("You are a helpful assistant."),
        neat.user("Tell me a story about a brave knight."),
    ]

def main():
    stream = generate_text()
    for chunk in stream:
        print(chunk, end='')

if __name__ == "__main__":

    main()