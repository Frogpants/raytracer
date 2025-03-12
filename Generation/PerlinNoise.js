
pList = [];

function randVal(a,b) {
    return a + (b-a+1)*Math.random()
};

function genList(length) {
    for (let i = 0; i < length; i++) {
        pList.push(randVal(35,80));
    }
};

function easeCurve(x) {
    return x*Math.cos(x);
};

function interpolate(n,p,t) {
    return (p*t)+(n*(1-t));
};

function perlin(x) {
    var p = 1-cos(180*(x-Math.floor(x)));
    p = interpolate(pList[Math.floor(x)],pList[Math.floor(x)+1],p)
    return p;
};

function calcPerlin(x,y) {
    var height = 0;
    height = perlin(x*Math.sin(y));
    height += perlin(y*Math.cos(x));
    return height;
};

function generatePerlin(width,height) {
    genList(width*height);
    var result = [];
    for (let y = 0; y < height; y++) {
        var list = [];
        for (let x = 0; x < width; x++) {
            list.push(calcPerlin(x,y));
        }
        result.push(list);
    }
    return result;
};