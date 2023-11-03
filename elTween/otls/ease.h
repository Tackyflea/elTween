float ease(string type; float t; float props[]; float time){
  //  if(t>1){t=1;};if(t<0){t=0;};
    if(type=="QuadIn"){
     return t*t;
    }else if(type=="QuadOut"){
     return t*(2-t);
    } else if(type=="QuadInOut"){
     return  t<.5 ? 2*t*t : -1+(4-2*t)*t;
    }else if(type=="CubicIn"){
     return t* t*t*t;
    }else if(type=="CubicOut"){
     return  (--t)*t*t+1;
    }else if(type=="CubicInOut"){
     return t<.5 ? 4*t*t*t : (t-1)*(2*t-2)*(2*t-2)+1;
    }else if(type=="QuartIn"){
     return  t*t*t*t;
    }else if(type=="QuartOut"){
     return  1-(--t)*t*t*t;
    }else if(type=="QuartInOut"){
     return  t<.5 ? 8*t*t*t*t : 1-8*(--t)*t*t*t;
    }else if(type=="QuintIn"){
     return t*t*t*t*t ;
    }else if(type=="QuintOut"){
     return 1+(--t)*t*t*t*t ;
    }else if(type=="QuintInOut"){
     return t<.5 ? 16*t*t*t*t*t : 1+16*(--t)*t*t*t*t ;
    }
    else if(type=="ElasticIn"){
      float pi2 = 3.1415926*2;
      float s0;
       if (props[1] == 0) props[1] = time * 0.3f;
       if (props[0] < 1) {
           props[0] = 1;
           s0 = props[1] / 4;
       } else {
         s0 = props[1] / pi2 * (float)asin(1 / props[0]);
       };
       return -(props[0] * (float)pow(2, 10 * (t -= 1)) * (float)sin((t * time - s0) * pi2 / props[1]));

    }  else if(type=="ElasticOut"){
        float pi2 = 3.1415926*2;
        float s1;
         if (props[1] == 0) props[1] = time * 0.3f;
         if (props[0] < 1) {
             props[0] = 1;
             s1 = props[1] / 4;
         } else {
           s1 = props[1] / pi2 * (float)asin(1 / props[0]);
         };
         return (props[0] * (float)pow(2, -10 * t) * (float)sin((t * time - s1) * pi2 / props[1]) + 1);

    }
    else if(type=="ElasticInOut"){

        float pi2 = 3.1415926*2;
      float s;
        if (props[1] == 0) props[1] = time * (0.3f * 1.5f);
        if (props[0] < 1) {
            props[0] = 1;
            s = props[1] / 4;
        } else{ s = props[1] / pi2 * (float)asin(1 / props[0]);};
        if (time < 1) return -0.5f * (props[0] * (float)pow(2, 10 * (t -= 1)) * (float)sin((t * time - s) * pi2 / props[1]));
        return props[0] * (float)pow(2, -10 * (t -= 1)) * (float)sin((t * time - s) * pi2 / props[1]) * 0.5f + 1;

   }else{
        return t;
    };
};
/* Test Example

float progress = 0.5;
string ease="linear";
float easeprops[] = {.5,.7};
float fsddf = ease("QuadOut",progress,easeprops, @Time );

*/
