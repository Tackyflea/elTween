float tpmt(float x){ return (pow(2, -10 * x) - 0.0009765625) * 1.0009775171065494; }; // used for elastic

 float bEaseOut(float t){
        float b1 = 4 / (float)11, b2 = (float)6 / (float)11, b3 = (float)8 / (float)11,
        b4 = (float)3 / (float)4, b5 = (float)9 / (float)11, b6 = (float)10 / (float)11,
        b7 = (float)15 / (float)16, b8 = (float)21 / (float)22, b9 = (float)63 / (float)64;
        float   b0 = 1 / b1 / b1;
       return (t = +t) < b1 ? b0 * t * t : t < b3 ? b0 * (t -= b2) * t + b4 : t < b6 ? b0 * (t -= b5) * t + b7 : b0 * (t -= b8) * t + b9;
}; //used for bounce
float ease(string type; float t; float props[]; float time)
{
  //  if(t>1){t=1;};if(t<0){t=0;};
  if (type == "Power1In")
  {
    return t * t;
  }
  else if (type == "Power1Out")
  { //power1
    return t * (2 - t);
  }
  else if (type == "Power1InOut")
  {
    return t < .5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
  }
  else if (type == "Power2In")
  {
    return t * t * t * t;
  }
  else if (type == "Power2Out")
  { //power2
    return (--t) * t * t + 1;
  }
  else if (type == "Power2InOut")
  {
    return t < .5 ? 4 * t * t * t : (t - 1) * (2 * t - 2) * (2 * t - 2) + 1;
  }
  else if (type == "Power3In")
  {
    return t * t * t * t;
  }
  else if (type == "Power3Out")
  { //power3
    return 1 - (--t) * t * t * t;
  }
  else if (type == "Power3InOut")
  {
    return t < .5 ? 8 * t * t * t * t : 1 - 8 * (--t) * t * t * t;
  }
  else if (type == "Power4In")
  {
    return t * t * t * t * t;
  }
  else if (type == "Power4Out")
  { //power4
    return 1 + (--t) * t * t * t * t;
  }
  else if (type == "Power4InOut")
  {
    return t < .5 ? 16 * t * t * t * t * t : 1 + 16 * (--t) * t * t * t * t;
  }
  else if (type == "ExpoIn")
  {
    if (t == 0)
    {
      return 0;
    }
    return pow(2, 10 * (t - 1));
  }
  else if (type == "ExpoOut")
  { //Expo
    if (t == 1)
    {
      return 1;
    }
    return 1 - pow(2, -10 * t);
  }
  else if (type == "ExpoInOut")
  {
    if (t == 0 || t == 1)
    {
      return t;
    }
    if (t < 0.5)
    {
      return 0.5 * pow(2, (20 * t) - 10);
    }
    return -0.5 * pow(2, (-20 * t) + 10) + 1;
  }
  else if (type == "ElasticOut")
  {
    float p = props[0], a = props[1];
    float s = asin(1 / (a = max(1, a))) * (p /= PI*2);
    return 1 - a * tpmt(t = +t) * sin((t + s) / p);
  }
  else if (type == "ElasticIn")
  {
    float p = props[0], a = props[1];
    float s = asin(1 / (a = max(1, a))) * (p /= PI*2);
    return a * tpmt(-(--t)) * sin((s - t) / p);
  }
  else if (type == "ElasticInOut")
  {

    float p = props[0], a = props[1];
    float s = asin(1 / (a = max(1, a))) * (p /= PI*2);
    return ((t = t * 2 - 1) < 0
      ? a * tpmt(-t) * sin((s - t) / p)
      : 2 - a * tpmt(t) * sin((s + t) / p)) / 2;
  }
  else if (type == "BounceIn")
  {
    float bT = 1-t;
   return 1-bEaseOut(bT) ;
  }
  else if (type == "BounceOut")
  {
    return bEaseOut(t);
  }
  else if (type == "BounceInOut")
  {
    float bT = 1-t;
      float bT2 = t-1;
      return ((t *= 2) <= 1 ? 1 - bEaseOut(bT) : bEaseOut(bT2) + 1) / 2;
  }
  else if (type == "BackIn")
  {
    return (t = +t) * t * (abs(props[0]) * (t - 1) + t);
  }
  else if (type == "BackOut")
  {
    return --t * t * ((t + 1) * abs(props[0]) + t) + 1;
  }
  else if (type == "BackInOut")
  {
    float s = abs(props[0]);
    return ((t *= 2) < 1 ? t * t * ((s + 1) * t - s) : (t -= 2) * t * ((s + 1) * t + s) + 2) / 2;
  }
  else
  {
    return t;
  };
};
/* Test Example

float progress = 0.5;
string ease="linear";
float easeprops[] = {.5,.7};
float fsddf = ease("QuadOut",progress,easeprops, @Time );

*/
