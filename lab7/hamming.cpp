// Hamming Code Error Detection
// Varsha Tumburu (1901CS69)
#include <bits/stdc++.h>
using namespace std;

// Function to generate hamming code
vector<int> generateHammingCode(vector<int> msgBits, int m, int r)
{
	// Stores the Hamming Code
	vector<int> hammingCode(r + m);

	// Find positions of redundant bits
	for (int i = 0; i < r; ++i)
	{
		// Placing -1 at redundant bits for easy identification
		int k = 1 << i;
		hammingCode[r + m - k] = -1;
	}

	int j = 0;
	cout << "Encoded format: ";
	// Update data bits into remaining bits
	for (int i = 0; i < (r + m); i++)
	{
		if (hammingCode[i] != -1) // Not a redundant bit (data bit)
		{
			cout << "D" << r + m - i << " ";
			hammingCode[i] = msgBits[j];
			j++;
		}
		else // Redundant/parity bit
			cout << "R" << r + m - i << " ";
	}
	cout << endl;

	// Setting the redundant/parity bits based on data bits
	// Using even parity here
	for (int i = 0; i < r; i++)
	{
		int k = 1 << i;
		int ans = 0;
		// For each power of 2, find parity bit and store
		for (int j = 0; j < r + m - k; j++)
		{
			if (hammingCode[j] == -1)
				continue;
			int p = r + m - j;
			if (k & p)
			{
				ans ^= hammingCode[j]; // xor operation
			}
		}
		hammingCode[r + m - k] = ans;
	}

	// Return the generated code
	return hammingCode;
}

// Function to find the hamming code of the given message bit msgBit[]
int findHammingCode(vector<int> &msgBit)
{

	// Message bit size
	int m = msgBit.size();

	// r is the number of redundant bits
	int r = 1;

	// Find no. of redundant bits
	while (pow(2, r) < (m + r + 1))
		r++;

	// Print the code
	cout << "Message bits are: ";
	for (int i = 0; i < msgBit.size(); i++)
		cout << msgBit[i] << " ";
	cout << endl;

	// Generating Code
	vector<int> ans = generateHammingCode(msgBit, m, r);

	// Print final answer
	cout << "Hamming code is: ";
	for (int i = 0; i < ans.size(); i++)
		cout << ans[i] << " ";

	// Return no. of redundant bits for error correction purposes
	return r;
}

// Function to find the position of single bit error given message and number of redundant bits
int findErrorBit(string e, int rb)
{
	// Convert string to vector of bits
	vector<int> bits;
	for (auto x : e)
	{
		if (x == '0')
			bits.push_back(0);
		else
			bits.push_back(1);
	}
	int len = e.length();

	// Here, errBit denotes which bit has been flipped, given there is only a single bit error in the message
	int errBit = 0;
	// For each power of 2, check if there's an error with the parity
	for (int i = 0; i < rb; i++)
	{
		int k = 1 << i;
		int ans = 0;
		for (int j = 1; j <= len; j++)
		{
			if (j & k)
				ans ^= bits[len - j];
		}
		// If error is present then ans=1, otherwise 0
		errBit += k * ans;
	}

	return errBit;
}

// Driver Code
int main()
{
	// Given message bits
	string msg, err;
	cout << "Enter message in binary: ";
	cin >> msg;

	// Sanitize inputs
	vector<int> msgBit;
	for (auto x : msg)
	{
		if (x == '0')
			msgBit.push_back(0);
		else
			msgBit.push_back(1);
	}

	// Function Call
	int rb = findHammingCode(msgBit);

	// Take another input (Error detection for same message)
	cout << endl
		 << "Enter erroneous message for the above: ";
	cin >> err;
	int len = err.length();

	// Find error bit
	int bit = findErrorBit(err, rb);
	if (bit == 0){
		cout << "Message received. No error found. " << endl;
		return 0;
	}
	cout << "Error on bit number " << bit << endl;

	// Flip wrong bit
	if (err[len - bit] == '0')
		err[len - bit] = '1';
	else
		err[len - bit] = '0';
	cout << "Corrected message: " << err << endl;

	return 0;
}
