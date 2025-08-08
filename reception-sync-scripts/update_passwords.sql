-- Atualização de senhas dos usuários
-- Execute este arquivo no Supabase SQL Editor

UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$YC6FvybqZHeazQbk$433c842b28cb9de63a01db80ce8e0791fcabcb00272168b3b868d54ef0fb21b07a6241ddb733407a984fb3fe63a0311e596f15bc104b3ac69628e51172c9122f' WHERE username = 'gerencia';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$HkwCGfipKKDuGj5k$b9f4116721cf5a29843890f32f608435767260ccd3535f7017fc28dc8bfdfba0fada01fe135f1611f99282e3efd03d437f9a8164be8df5509a662854e1d782e9' WHERE username = 'admpodd';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$ZEgsbgyFzfuJ66BB$4f0c607db318280e574fe2e3015a3eb68f0a48cfea5ed426fff3880bec35381e52093e9ebfb7bd6c73bd52ce7345a58604de78159b51aa7172b38955a99e4b6a' WHERE username = 'admpdg';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$YcZaYXcmVk8zDkzx$9819ab18ad886b1b898be999d94c8f10b84a0b86286ace1f7424f86f307730884e8ca7d9014cba24e8185404a20e320a2a89870ba6c39320d26014cd32fd7cf8' WHERE username = 'admaba';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$NwdJBv7nqFQHGjfL$ea9b70d76a8956b450b7308fe2784bb9a4073f9fdabf68c38ab37eeb842cb3904a5e90a83b505ffd5e0f369cfa0775662a7f7ee2f84c2d9bb40bafc6faeb622e' WHERE username = 'recepcao103';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$34TT62gTdTE6Eavw$2ce5af6671fdbae9f9f3814b83925d60169ac91b68c1557d23227b9c7880c41ab32f72a71bffa8e9f831cc987c30e8c64ae66518cd5c941501022ece849eae01' WHERE username = 'recepcao108';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$z9kop9KnXzAuOAW6$d82081f5a9efeb49c85587e73a24ebe3f3b9d8e7bcc731db580a4702fd36e003b65b70f122f305e008dcd1b111029c9d83362a78a7bec8dc8c500f2d680b9739' WHERE username = 'recepcao203';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$uCDWQINQ86Aft8nk$0b3a6e5a501d2d813a9e03f16901c4c76bf85aacd6b147548fe84b35173a11a6918baecca6a4fd23a702f7986c503478047cc6b9a65296ea573ec1f7afe50427' WHERE username = 'recepcao808';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$J9X5VvR0iiTVXpwy$b9caad90f5aa74ad007d48c55f71ea4c64666c14bce11c73251dba7a79af2a7a6424d45a76c7a862147ebe412ef6f6be7b361ac220255f84003f48f7669b14c7' WHERE username = 'recepcao1002';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$B9sJ9eRyIfPj7qQ3$c7e84887332d8316f46f0818cce1fa1cbc8466239bd330ba9712a9c02a95e5848ceecc0d0310b95a0db6669f7d6f13cca9f5139ceffe8362a77b79e298facc2f' WHERE username = 'recepcao1009';
UPDATE usuarios SET password_hash = 'scrypt:32768:8:1$TIx9RCej4tqIl8Tr$458cbffd056f6a049659e9a799effae0db3c47bd5ca0d40c6fe0510a1b1012d59497ebe90a09021c6d4e9460780cefa865f0f3e8b03cf3732eeeda1669805ccb' WHERE username = 'recepcao1108';

-- Verificar atualizações
SELECT username, email, role, LEFT(password_hash, 20) || '...' as hash_preview FROM usuarios ORDER BY username;
