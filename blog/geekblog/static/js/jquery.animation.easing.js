jQuery.easing['jswing'] = jQuery.easing['swing'];

jQuery.extend({
    easing:
    {
        def: 'easeOutQuad',
        swing: function (x, t, b, c, d) {
            //alert(jQuery.easing.default);
            return jQuery.easing[jQuery.easing.def](x, t, b, c, d);
        },
        easeInQuad: function (x, t, b, c, d) {
            return c*(t/=d)*t + b;
        },
        easeOutQuad: function (x, t, b, c, d) {
            return -c *(t/=d)*(t-2) + b;
        },
        easeInOutQuad: function (x, t, b, c, d) {
            if ((t/=d/2) < 1) return c/2*t*t + b;
            return -c/2 * ((--t)*(t-2) - 1) + b;
        },
        easeInCubic: function (x, t, b, c, d) {
            return c*(t/=d)*t*t + b;
        },
        easeOutCubic: function (x, t, b, c, d) {
            return c*((t=t/d-1)*t*t + 1) + b;
        },
        easeInOutCubic: function (x, t, b, c, d) {
            if ((t/=d/2) < 1) return c/2*t*t*t + b;
            return c/2*((t-=2)*t*t + 2) + b;
        },
        easeInQuart: function (x, t, b, c, d) {
            return c*(t/=d)*t*t*t + b;
        },
        easeOutQuart: function (x, t, b, c, d) {
            return -c * ((t=t/d-1)*t*t*t - 1) + b;
        },
        easeInOutQuart: function (x, t, b, c, d) {
            if ((t/=d/2) < 1) return c/2*t*t*t*t + b;
            return -c/2 * ((t-=2)*t*t*t - 2) + b;
        },
        easeInQuint: function (x, t, b, c, d) {
            return c*(t/=d)*t*t*t*t + b;
        },
        easeOutQuint: function (x, t, b, c, d) {
            return c*((t=t/d-1)*t*t*t*t + 1) + b;
        },
        easeInOutQuint: function (x, t, b, c, d) {
            if ((t/=d/2) < 1) return c/2*t*t*t*t*t + b;
            return c/2*((t-=2)*t*t*t*t + 2) + b;
        },
        easeInSine: function (x, t, b, c, d) {
            return -c * Math.cos(t/d * (Math.PI/2)) + c + b;
        },
        easeOutSine: function (x, t, b, c, d) {
            return c * Math.sin(t/d * (Math.PI/2)) + b;
        },
        easeInOutSine: function (x, t, b, c, d) {
            return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b;
        },
        easeInExpo: function (x, t, b, c, d) {
            return (t==0) ? b : c * Math.pow(2, 10 * (t/d - 1)) + b;
        },
        easeOutExpo: function (x, t, b, c, d) {
            return (t==d) ? b+c : c * (-Math.pow(2, -10 * t/d) + 1) + b;
        },
        easeInOutExpo: function (x, t, b, c, d) {
            if (t==0) return b;
            if (t==d) return b+c;
            if ((t/=d/2) < 1) return c/2 * Math.pow(2, 10 * (t - 1)) + b;
            return c/2 * (-Math.pow(2, -10 * --t) + 2) + b;
        },
        easeInCirc: function (x, t, b, c, d) {
            return -c * (Math.sqrt(1 - (t/=d)*t) - 1) + b;
        },
        easeOutCirc: function (x, t, b, c, d) {
            return c * Math.sqrt(1 - (t=t/d-1)*t) + b;
        },
        easeInOutCirc: function (x, t, b, c, d) {
            if ((t/=d/2) < 1) return -c/2 * (Math.sqrt(1 - t*t) - 1) + b;
            return c/2 * (Math.sqrt(1 - (t-=2)*t) + 1) + b;
        },
        easeInElastic: function (x, t, b, c, d) {
            var s=1.70158;var p=0;var a=c;
            if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
            if (a < Math.abs(c)) { a=c; var s=p/4; }
            else var s = p/(2*Math.PI) * Math.asin (c/a);
            return -(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
        },
        easeOutElastic: function (x, t, b, c, d) {
            var s=1.70158;var p=0;var a=c;
            if (t==0) return b;  if ((t/=d)==1) return b+c;  if (!p) p=d*.3;
            if (a < Math.abs(c)) { a=c; var s=p/4; }
            else var s = p/(2*Math.PI) * Math.asin (c/a);
            return a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b;
        },
        easeInOutElastic: function (x, t, b, c, d) {
            var s=1.70158;var p=0;var a=c;
            if (t==0) return b;  if ((t/=d/2)==2) return b+c;  if (!p) p=d*(.3*1.5);
            if (a < Math.abs(c)) { a=c; var s=p/4; }
            else var s = p/(2*Math.PI) * Math.asin (c/a);
            if (t < 1) return -.5*(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b;
            return a*Math.pow(2,-10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )*.5 + c + b;
        },
        easeInBack: function (x, t, b, c, d, s) {
            if (s == undefined) s = 1.70158;
            return c*(t/=d)*t*((s+1)*t - s) + b;
        },
        easeOutBack: function (x, t, b, c, d, s) {
            if (s == undefined) s = 1.70158;
            return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
        },
        easeOutBackSmall: function (x, t, b, c, d, s) {
            if (s == undefined) s = 1;
            return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b;
        },
        easeInOutBack: function (x, t, b, c, d, s) {
            if (s == undefined) s = 1.70158; 
            if ((t/=d/2) < 1) return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b;
            return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b;
        },
        easeInBounce: function (x, t, b, c, d) {
            return c - jQuery.easing.easeOutBounce (x, d-t, 0, c, d) + b;
        },
        easeOutBounce: function (x, t, b, c, d) {
            if ((t/=d) < (1/2.75)) {
                return c*(7.5625*t*t) + b;
            } else if (t < (2/2.75)) {
                return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b;
            } else if (t < (2.5/2.75)) {
                return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b;
            } else {
                return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b;
            }
        },
        easeInOutBounce: function (x, t, b, c, d) {
            if (t < d/2) return jQuery.easing.easeInBounce (x, t*2, 0, c, d) * .5 + b;
            return jQuery.easing.easeOutBounce (x, t*2-d, 0, c, d) * .5 + c*.5 + b;
        },
        // ******* back
        backEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            var s = 1.70158; // default overshoot value, can be adjusted to suit
            return c*(p/=1)*p*((s+1)*p - s) + firstNum;
        },
        backEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            var s = 1.70158; // default overshoot value, can be adjusted to suit
            return c*((p=p/1-1)*p*((s+1)*p + s) + 1) + firstNum;
        },
        backEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            var s = 1.70158; // default overshoot value, can be adjusted to suit
            if ((p/=0.5) < 1) 
                return c/2*(p*p*(((s*=(1.525))+1)*p - s)) + firstNum;
            else
                return c/2*((p-=2)*p*(((s*=(1.525))+1)*p + s) + 2) + firstNum;
        },
        // ******* bounce
        bounceEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            var inv = this.bounceEaseOut (1-p, 1, 0, diff);
            return c - inv + firstNum;
        },
        bounceEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if (p < (1/2.75))
            {
                return c*(7.5625*p*p) + firstNum;
            }
            else if (p < (2/2.75))
            {
                return c*(7.5625*(p-=(1.5/2.75))*p + .75) + firstNum;
            }
            else if (p < (2.5/2.75))
            {
                return c*(7.5625*(p-=(2.25/2.75))*p + .9375) + firstNum;
            }
            else
            {
                return c*(7.5625*(p-=(2.625/2.75))*p + .984375) + firstNum;
            }
        },
        // ******* circ
        circEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return -c * (Math.sqrt(1 - (p/=1)*p) - 1) + firstNum;
        },
        circEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c * Math.sqrt(1 - (p=p/1-1)*p) + firstNum;
        },
        circEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if ((p/=0.5) < 1) 
                return -c/2 * (Math.sqrt(1 - p*p) - 1) + firstNum;
            else
                return c/2 * (Math.sqrt(1 - (p-=2)*p) + 1) + firstNum;
        },
        // ******* cubic
        cubicEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*(p/=1)*p*p + firstNum;
        },
        cubicEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*((p=p/1-1)*p*p + 1) + firstNum;
        },
        cubicEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if ((p/=0.5) < 1)
                return c/2*p*p*p + firstNum;
            else
                return c/2*((p-=2)*p*p + 2) + firstNum;
        },
        // ******* elastic
        elasticEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if (p==0) return firstNum;
            if (p==1) return c;

            var peroid = 0.25;
            var s;
            var amplitude = c;
            if (amplitude < Math.abs(c)) 
            {
                amplitude = c;
                s = peroid/4;
            } 
            else 
            {
                s = peroid/(2*Math.PI) * Math.asin (c/amplitude);
            }
            return -(amplitude*Math.pow(2,10*(p-=1)) * Math.sin( (p*1-s)*(2*Math.PI)/peroid )) + firstNum;
        },
        elasticEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if (p==0) return firstNum;
            if (p==1) return c;
            var peroid = 0.25;
            var s;
            var amplitude = c;
            if (amplitude < Math.abs(c)) 
            {
                amplitude = c;
                s = peroid/4;
            }
            else
            {
                s = peroid/(2*Math.PI) * Math.asin (c/amplitude);
            }

            return -(amplitude*Math.pow(2,-10*p) * Math.sin( (p*1-s)*(2*Math.PI)/peroid )) + c;
        },
        // ******* expo
        expoEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return (p==0) ? firstNum : c * Math.pow(2, 10 * (p - 1)) + firstNum - c * 0.001;
        },
        expoEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return (p==1) ? c : diff * 1.001 * (-Math.pow(2, -10 * p) + 1) + firstNum;
        },
        expoEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if (p==0) return firstNum;
            if (p==1) return c;
            if ((p/=0.5) < 1) 
                return c/2 * Math.pow(2, 10 * (p - 1)) + firstNum - c * 0.0005;
            else
                return c/2 * 1.0005 * (-Math.pow(2, -10 * --p) + 2) + firstNum;
        },
        // ******* quad
        quadEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*(p/=1)*p + firstNum;
        },
        quadEaseOut:function(p, n, firstNum, diff) {

            var c=firstNum+diff;
            return -c *(p/=1)*(p-2) + firstNum;
        },
        quadEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if ((p/=0.5) < 1)
                return c/2*p*p + firstNum;
            else
                return -c/2 * ((--p)*(p-2) - 1) + firstNum;
        },
        // ******* quart
        quartEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*(p/=1)*p*p*p + firstNum;
        },
        quartEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return -c * ((p=p/1-1)*p*p*p - 1) + firstNum;
        },
        quartEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if ((p/=0.5) < 1) 
                return c/2*p*p*p*p + firstNum;
            else
                return -c/2 * ((p-=2)*p*p*p - 2) + firstNum;
        },
        // ******* quint
        quintEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*(p/=1)*p*p*p*p + firstNum;
        },
        quintEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c*((p=p/1-1)*p*p*p*p + 1) + firstNum;
        },
        quintEaseInOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            if ((p/=0.5) < 1)
                return c/2*p*p*p*p*p + firstNum;
            else
                return c/2*((p-=2)*p*p*p*p + 2) + firstNum;
        },
        // *******  sine
        sineEaseIn:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return -c * Math.cos(p * (Math.PI/2)) +c + firstNum; 
        },
        sineEaseOut:function(p, n, firstNum, diff) {
            var c=firstNum+diff;
            return c * Math.sin(p * (Math.PI/2)) + firstNum;
        },
        sineEaseInOut:function(p, n, firstNum, diff) {

            var c=firstNum+diff;
            return -c/2 * (Math.cos(Math.PI*p) - 1) + firstNum;
        }
    }
});
