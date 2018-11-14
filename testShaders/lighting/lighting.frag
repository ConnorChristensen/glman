#version 120

varying vec3 vColor, vN, vL, vE;
varying vec2 vST;

const float uShininess = 0.8, uKa = 0.3, uKd = 0.1, uKs = 0.1;
const vec3 uColor = vec3(0.0, 0.9, 0.9), uSpecularColor = vec3(1.0, 0.5, 0.5);


void main() {
  vec3 Normal = normalize(vN);
  vec3 Light  = normalize(vL);
  vec3 Eye    = normalize(vE);

  vec3 ambient = uKa * uColor;

  float d = max(dot(Normal, Light), 0.0);
  vec3 diffuse = uKd * d * uColor;
  float s = 0;

  if( dot(Normal,Light) > 0. ) {
    vec3 ref = normalize( reflect( -Light, Normal ) );
    s = pow( max( dot(Eye,ref),0. ), uShininess );
  }
  vec3 specular = uKs * s * uSpecularColor;
  gl_FragColor = vec4( ambient + diffuse + specular, 1. );
}
