#version 120

varying vec3 vColor, vN, vL, vE;
varying vec2 vST;
const vec3 LIGHTPOSITION = vec3(0.5, 0.5, 0.0);

void main() {
  vST = gl_MultiTexCoord0.st;
  vec4 ECposition = gl_ModelViewMatrix * gl_Vertex;
  vN = normalize(gl_NormalMatrix * gl_Normal);
  vL = LIGHTPOSITION - ECposition.xyz;
  vE = vec3(0.0, 0.0, 0.0) - ECposition.xyz;

  gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
