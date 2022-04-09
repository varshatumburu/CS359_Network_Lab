// CRC Error Detection
// Varsha Tumburu (1901CS69)
#include <bits/stdc++.h>
using namespace std;

// Returns binary string on xor of 2 other binary strings
string exor(string a, string b)
{
	string ans = "";
	int l = a.length();
	for (int i = 0; i < l; i++)
	{
		if (a[i] == b[i])
			ans.push_back('0');
		else
			ans.push_back('1');
	}
	return ans.substr(1, l - 1);
}

// Function to generate CRC code given message and divisor
void generateCRC(string data, string key)
{
	// Length of message and code
	int datalen = data.length();
	int keylen = key.length();

	// Append keylen-1 0s to data so that it can be replaced by CRC in the end
	data.append(keylen - 1, '0');

	// Total code length
	int codelen = datalen + keylen - 1;

	// Starting the division process
	cout << "Binary division process:" << endl;
	// temp is always the dividend while key is the divisor
	string temp = data.substr(0, keylen), rem = "";

	for (int j = keylen; j <= codelen; j++)
	{
		// If dividend<divisor then move on to next bit
		if (rem[0] == '0')
			rem = temp.substr(1, keylen - 1);
		// divide by xor
		else
			rem = exor(temp, key);
		cout << "Current dividend= " << temp << " Remainder= " << rem << endl;
		// If not last step, then append new bit
		if (j != codelen)
			rem += data[j];
		// Update dividend to remainder
		temp = rem;
	}
	// Update last keylen-1 bits of data with CRC
	for (int i = 0; i < keylen - 1; i++)
		data[datalen + i] = rem[i];

	cout << "CRC=" << rem << "\nDataword=" << data << endl;
}

// Function to detect error through CRC
void detectError(string data, string key)
{
	int keylen = key.length(), datalen = data.length();
	string temp = data.substr(0, keylen), rem;
	// cout << "Binary division process:" << endl;

	// Follow the same divison process again with data as dividend and key as divisor
	for (int j = keylen; j <= datalen; j++)
	{
		if (rem[0] == '0')
			rem = temp.substr(1, keylen - 1);
		else
			rem = exor(temp, key);
		// cout << "Current dividend= " << temp << " Remainder= " << rem << endl;
		if (j != datalen)
			rem += data[j];
		temp = rem;
	}
	// If remainder is 0, then there is no error in the message transmitted
	if (rem != "0000")
		cout << "Error detected! Message has been corrupted." << endl;
	// Otherwise there is some error in the data received
	else
		cout << "Message perfectly transmitted. No errors!" << endl;
}

int main()
{
	string divisor, data, errmsg;

	// Generate CRC code
	cout << "Enter the data:";
	cin >> data;
	cout << "Enter the key/divisor:";
	cin >> divisor;
	generateCRC(data, divisor);

	// Detect any error in message
	cout << "Enter erroneous message for the same: ";
	cin >> errmsg;
	detectError(errmsg, divisor);

	return 0;
}
