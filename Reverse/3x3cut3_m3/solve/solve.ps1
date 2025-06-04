# Clé XOR utilisée pour l'encodage
$xorKey = @(42, 17, 99, 84, 63, 19, 88, 7, 31, 55, 91, 12, 33, 20, 75, 11)

# Résultat chiffré attendu
$expectedEncoded = @(93, 72, 28, 24, 67, 23, 98, 58, 35, 75, 98, 87, 68, 30, 97, 33)

# Longueur du nom d'utilisateur au moment du chiffrement
for ($usernameLength = 0; $usernameLength -lt 20; $usernameLength++) {
    # Tableau pour stocker les caractères décodés
    $decodedChars = @()

    # Décodage
    for ($i = 0; $i -lt $expectedEncoded.Length; $i++) {
        $enc = $expectedEncoded[$i]
        $key = $xorKey[$i]
        $val = ($enc + $usernameLength) % 169
        $ascii = $val -bxor $key
        $decodedChars += [char]$ascii
    }

    # Affichage du mot de passe
    $decodedPassword = -join $decodedChars
    Write-Output "Mot de passe décodé : $decodedPassword"
}