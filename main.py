if __name__ == "__main__":
    from models.client import run
    import json

    token_file = json.load(open("token.json" , "r"))

    run(token=token_file['token'])