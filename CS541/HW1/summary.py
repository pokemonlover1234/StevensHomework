import pandas as pd
import statistics

def summary_statistics(state):
    #Start your code implementation from here
    df = pd.read_csv("us-states.csv")
    # Make sure state is in data
    if not state in df["state"].unique():
        raise ValueError("State not found in data. Make sure you provide a valid U.S. state.")
    values = df[df["state"] == state]["cases"].tolist()
    return min(values), max(values), statistics.mean(values), statistics.pstdev(values)

def main():
    #The output should contain Minimum, Maximum, Standard deviation and Mean, each data in separate line in below given order:
    #Minimum:
    #Maximum:
    #Mean:
    #Standard Deviation:
    state = input("Enter a U.S. state: ")
    # Make sure state is capitalized properly
    stateparts = state.split(" ")
    for i in range(len(stateparts)):
        stateparts[i] = stateparts[i][0].upper() + stateparts[i][1:].lower()
    state = " ".join(stateparts)
    # Get the summary
    mini, maxi, avg, std = summary_statistics(state)
    print(f"Minimum: {mini}\nMaximum: {maxi}\nMean: {avg}\nStandard Deviation: {std}")
    

if __name__ == "__main__":
    main()