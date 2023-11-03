float fetchTime(float time, over_time,stagger, distance, delay,el_s,el_d){
    //subtract the stagger from the time so it fits within the range
    over_time-=stagger*distance;
    //movement over time
    float delayed_time = time - el_d;
    delayed_time-=delay;
    float progress_raw =  (delayed_time/ over_time)*el_s;
    float t=clamp(progress_raw,0,1);
return t;
}; 
