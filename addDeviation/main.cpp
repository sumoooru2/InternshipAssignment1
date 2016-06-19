#include<iostream>
#include<vector>
#include<cmath>
#include<sstream>
#include<numeric>

using namespace std;
using ll = long long;

int main(){
	string name, num;
	vector<string> names;
	vector<ll> nums;
	istringstream iss;
	while(cin >> name >> num){
		names.push_back(name);
		*remove(num.begin(), num.end(), ',') = '\0';
		iss.clear();
		iss.str(num.c_str());
		ll n;
		iss >> n;
		nums.push_back(n);
		// cout<<name<<' '<<atoi(num.c_str())<<endl;
	}

	double avg = accumulate(nums.begin(), nums.end(), 0.0) / nums.size(),
		   sd = 0;
	for(ll n : nums){
		sd += (n - avg) * (n - avg);
	}
	sd /= nums.size();
	sd = sqrt(sd);
	// cout<<avg<<' '<<sd<<endl;

	for(int i=0;i<nums.size();i++){
		cout << names[i] << '\t' << nums[i] << '\t' << (50 + 10 * (nums[i] - avg) / sd) << endl;
	}
	return 0;
}
