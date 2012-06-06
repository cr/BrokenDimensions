 
    // precision highp float;
    
    uniform float MyIter;
    uniform float MyTime;
    varying vec4 MyCoord4f;

    float hue2rgb( float p, float q, float t ) {

        if( t < 0.0 ) t += 1.0;
        if( t > 1.0 ) t -= 1.0;
        if( t < 1.0/6.0 ) return p + (q - p) * 6.0 * t;
        if( t < 1.0/2.0 ) return q;
        if( t < 2.0/3.0 ) return p + (q - p) * (2.0/3.0 - t) * 6.0;
        return p;
    }

    void main() {

        vec2 z, c;

        // chose b/w mandelbrot and julia set

        //c.x = MyCoord4f.x;
        //c.y = MyCoord4f.y;
        c.x = 0.3;
        c.y = 0.0;

        z.x = MyCoord4f.x;
        z.y = MyCoord4f.y;

        float wobble = 1.0+sin(length(MyCoord4f)*10.0+MyTime*6.0)*0.03;

        //funny accident, looks great with julia
        //float wobble = 1.0+sin(length(c)*10.0+MyTime*6.0)*0.03;

        c *= wobble;
        z *= wobble;

        float i = 0.0;
        while( i < MyIter ) {

            float x = ( z.x * z.x - z.y * z.y ) + c.x;
            float y = ( z.x * z.y + z.y * z.x ) + c.y;

            if( ( x * x + y * y ) > 4.0 ) break;

            z.x = x;
            z.y = y;
            i += 1.0;
        }

        // a color scheme from the Orange Book OpenGLSL 2nd Edition
        vec3 color;
        if ( i == MyIter ) {
            color = vec3( 0.0, 0.3, 0.8 );
        } else { // i.e. z is going towards infinity, show how fast
            color = mix( vec3( 0.65, 0.25, 0.25 ), vec3( 0.7, 0.65, 0.1 ), fract( i * 0.05 ));
            // color = mix( vec3( 0.0, 0.3, 0.8 ), vec3( 0.75, 0.25, 0.25 ), fract( i * 0.1 ));
        }
        gl_FragColor = vec4( color, 1.0 );
        

        // another color scheme: black n white, modern
        // float sq = z.x * z.x + z.y * z.y;
        // gl_FragColor = vec4( sq, sq, sq, 1.0 );
        

        // // just another color mapping ( remove break condition in while loop! )
        // // take polar coordinates of z with length as hue, angle as lightness
        // float pi = 3.141592653589793238462643383279;    // a manual pi  0_o
        // float absZ, argZ;
        // absZ = sqrt( z.x * z.x + z.y * z.y );
        // argZ = atan( z.y, z.x ) / ( 2.0 * pi );

        // float H, S, V;
        // H = absZ;               // original: argZ
        // V = absZ;               // original: absZ
        // S = 1.0;

        // float q = ( ( V < 0.5 ) ? ( V * ( 1.0 + S )) : ( V + S - V * S ));
        // float p = 2.0 * V - q;  // default: 2.0 * V - q;  cheesy: - q;
        // float R, G, B;
        // R = hue2rgb( p, q, H + 1.0 / 3.0 );
        // G = hue2rgb( p, q, H );
        // B = hue2rgb( p, q, H - 1.0 / 3.0 );

        // gl_FragColor = vec4( R, G, B, 1.0 );

    }
