// Script to generate client_secret.rb
require 'jwt'

key_file = 'AuthKey_YOUR_KEY_ID.p8'
team_id = 'VRCK9ZBZG6'
client_id = 'com.emre.utrack.app'
key_id = 'YOUR_KEY_ID'

ecdsa_key = OpenSSL::PKey::EC.new IO.read key_file

headers = {
  'kid' => key_id
}

claims = {
  'iss' => team_id,
  'iat' => Time.now.to_i,
  'exp' => Time.now.to_i + 86400*180, # 180 days
  'aud' => 'https://appleid.apple.com',
  'sub' => client_id,
}

token = JWT.encode claims, ecdsa_key, 'ES256', headers

puts token
