
	uniform float MyIter;
	varying vec4 MyCoord4f;

	void main() {

		// get eye coordinates
		MyCoord4f = gl_ModelViewMatrix * gl_Vertex;

		gl_Position = ftransform();

	}
