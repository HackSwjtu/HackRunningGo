#include <bits/stdc++.h>
using namespace std;

const double eps = 1e-8;

const double PI = 3.1415926535897932384626;

#define END_STR							"----------------"
#define EDGE_MAX_DIS					50
#define OK_POINT_SIZE					16

fstream input, output;

double radian(double d){
	return d * PI / 180.0;
}

class Point{
public:
	double lat,lng;
	Point(double lng, double lat):lat(lat),lng(lng){}
	Point():lat(0),lng(0){}

	bool operator ==(Point &p){
		return (fabs(p.lat - lat)<eps && fabs(p.lng - lng)<eps );
	}
	
	bool operator<(Point p)const{
		return true;
	}	

	double disToPoint(Point &p){
		double radLat1 = radian(lat);
		double radLat2 = radian(p.lat);
		double a = radLat1 - radLat2;
		double b = radian(lng) - radian(p.lng);
		double s = 2 * asin(sqrt(pow(sin(a/2),2) + 
					   cos(radLat1)*cos(radLat2)*pow(sin(b/2),2)));
		s = s * 6378.137;
		return s * 1000;
	}
	/*get the distance between tow point whit return value in mile*/

};

vector<Point>okV;
vector<Point>V;
vector<string>fivePointJson;
void init(){
	okV.push_back(Point(103.985729,30.771025));
	okV.push_back(Point(103.987364,30.768690));
	okV.push_back(Point(103.988141,30.772452));
	okV.push_back(Point(103.989982,30.768566));
	okV.push_back(Point(103.990072,30.765339));
	okV.push_back(Point(103.990113,30.775152));
	okV.push_back(Point(103.991393,30.769404));
	okV.push_back(Point(103.991707,30.763314));
	okV.push_back(Point(103.992839,30.767362));
	okV.push_back(Point(103.993903,30.772670));
	okV.push_back(Point(103.995718,30.773321));
	okV.push_back(Point(103.996032,30.766797));
	okV.push_back(Point(103.996949,30.770715));
	okV.push_back(Point(103.998134,30.768291));
	okV.push_back(Point(103.998840,30.766111));
	okV.push_back(Point(104.000061,30.774981));
}

string intToStr(long long x){
	string ret;
	if(x==0) ret = "0";
	else{
		while(x>0){
			ret = ret + (char)((x%10)+'0');
			x/=10;
		}
	}
	reverse(ret.begin(),ret.end());
	return ret;
}

string doubleToStr(double x){
	string ret = intToStr( (long long)x );
	x-=(long long)x;
	ret = ret + '.';
	double tmp = 0.1;
	for(int i = 0; i < 6; ++i){
		int ii = x/tmp;
		x-=ii*tmp;
		ret = ret + (char)(ii+'0');
		tmp/=10;
	}
	return ret;
}

void outPutFivePointJson(string tmps){
	set<Point>passP,ranP;
	int sz = V.size();
	for(int i = 0; i < OK_POINT_SIZE; ++i){
		for(int j = 0; j < sz; ++j){
			if(V[j].disToPoint(okV[i]) < EDGE_MAX_DIS){
				passP.insert(okV[i]);
				break;
			}
		}
		if(passP.size() == 3) break;
	}
	
	while(ranP.size() < 2){
		int t = rand()% OK_POINT_SIZE;
		if(!passP.count(okV[t]) && !ranP.count(okV[t]))
			ranP.insert(okV[t]);
	}

	int fix = rand()%3;
	string s = "{\"fivePointJson\":\"[";
	for(int i = 0; i < 5; ++i){
		int t;
		if(!ranP.empty() && !passP.empty()) t = rand()%2;
		else if (ranP.empty()) t = 1;
		else t = 0;
		Point tmpPoint;
		if(t==0){
			tmpPoint = *ranP.begin();
			ranP.erase(ranP.begin());
		}else{
			tmpPoint = *passP.begin();
			passP.erase(passP.begin());
		}
		s=s+"{\\\"flag\\\":"+tmps+",\\\"lon\\\":\\\""+doubleToStr(tmpPoint.lng)+"\\\",\\\"lat\\\":\\\"";
		s=s+doubleToStr(tmpPoint.lat);
		s=s+"\\\",\\\"isFixed\\\":";
		if(t == 1 && passP.size() == fix) s=s+"1";
		else s=s+"0";
		s=s+",\\\"isPass\\\":";
		if(t == 1) s = s + "true";
		else s = s + "false";
		s = s + ",\\\"isFinal\\\":false,\\\"id\\\":";
		s=s+intToStr(i+fix*100+5)+"}";
		if(i!=4) s=s+",";
	}
	
	s = s + "]\",\"useZip\":false}";
	
	fivePointJson.push_back(s);
}

double readDouble(string &s, int pos){
	double inte = 0, dec  = 0;
	while(s[pos] >= '0' && s[pos] <= '9'){
		inte = inte * 10 + s[pos] - '0';
		++pos;
	}
	++pos;
	double tmp = 0.1;
	while(s[pos] >= '0' && s[pos] <= '9'){
		dec = dec + tmp * (s[pos] - '0');
		++pos; tmp/=10;
	}
	return inte + dec;
}

string read(){
	V.clear();
	string flag;
	string allLocJson;
	if(input.eof()) return "NULL";
	input>>allLocJson;
	bool first = true;
	while(input>>allLocJson){
		if(first){
			int pos = allLocJson.find("flag");
			flag = allLocJson.substr(pos+7,13);
			//cerr<<flag<<"efdsf"<<endl;
			first = false;
		}
		if(allLocJson == END_STR)
			break;	
		
		int pos = allLocJson.find("lat");
		double lat = readDouble(allLocJson,pos+8);
		pos = allLocJson.find("lng");
		double lng = readDouble(allLocJson,pos+8);
		V.push_back(Point(lng,lat));
	} 
	return flag;
}

void work(){
	string flag;
	init();
	input.open("route.data");
	output.open("tp.data",ios::out);
	while(true){
		flag = read();
		if( flag == "NULL" ){
			bool first = true;
			for(auto it:fivePointJson){
				if(first){
					first = false;
					output<<it<<endl<<END_STR;
				}else{
					output<<endl<<it<<endl<<END_STR;
				}
			} 
			break;
		}
		outPutFivePointJson(flag);
	}
	input.close();
	output.close();
}


