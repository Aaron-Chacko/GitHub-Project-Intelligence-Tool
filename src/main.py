import pandas as pd

def main():
    df = pd.read_csv("data/input.csv")
    print("Data loaded successfully:\n")
    print(df)

if __name__ == "__main__":
    main()