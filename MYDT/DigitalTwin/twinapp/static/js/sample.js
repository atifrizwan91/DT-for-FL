"use strict";
// {index : { name : { color : time, ...}}}
let shiftObj = {
    "1" : {
        "get temperature ": [
            {"1" : "10:00-12:00"},
        ]
    },
    "2" : {
        " report temperature": [
            {"1" : "12:00-13:00"},
        ]
    },
    "500" : {
        "get humidity": [
            {"1" : "13:00-14:00"}
        ]
    },
    "3" : {
        "report humidity": [
            {"1" : "10:00-12:00"},
        ]
    },
    "4" : {
        "Get wind data": [

            {"1" : "14:00-17:30"},
        ]
    },
    "5" : {
        "Report wind data": [
            {"1" : "17:30-18:00"}
        ]
    },
    "6" : {
        " process sensing data": [
            {"1" : "19:00-22:30"}
        ]
    },
    "7" : {
        "compute fire intensity": [
            {"1" : "23:00-23:30"}
        ]
    },
    "8" : {
        "predict fire action": [
            {"1" : "10:00-12:00"},

        ]
    },
};
let obj = {
    // Beginning Time
    startTime: "01:00",
    // Ending Time
    endTime: "20:00",
    //Time to divide(hour),
    divTime: "15",
    // Time Table
    shift: shiftObj,
    // Other options
    option: {
        // workTime include time not displaying
        workTime: true,
        bgcolor: ["#00FFFF"],
        // {index :  name, : index: name,,..}
        // selectBox index and shift index should be same
        // Give randome if shift index was not in selectBox index
        selectBox: {
            /*"35" : "Jason Paige",
            "18" : "Mr.Jason",
            "25" : "Mrs.Jason",
            "38" : "A",
            "39" : "B",
            "40" : "C"*/
        },
        // Set false if you want the rows to be static i.e. as defined in your shift object
        deleteRows: true,
        // Set true when using TimeTable inside of BootStrap class row
        useBootstrap: false,
    }
};
// Call Time Table
var instance = new TimeTable(obj);
console.time("time"); // eslint-disable-line
instance.init("#test");
console.timeEnd("time");// eslint-disable-line

// Only works if selectBox option exist
$(document).on("click", "#addRow",()=>{instance.addRow();});

// Change theme color sample
$(document).on("click","#colorChange", ()=>{
    let color = `${getColor()},${getColor()},${getColor()}`;
    document.documentElement.style.setProperty("--rgbTheme", color);
});
function getColor(){
    return Math.floor(Math.random() * Math.floor(255));
}
// Getting Data Sample
$(document).on("click","#getData", ()=>{
    let data = instance.data();
    console.log(data);
});
