# Tableau servant de clé XOR
$xorKey = @(42, 17, 99, 84, 63, 19, 88, 7, 31, 55, 91, 12, 33, 20, 75, 11)

# Longueur du nom d'utilisateur
$usernameLength = ($env:USERNAME).Length

# Demande à l'utilisateur un mot de passe
$passwordInput = Read-Host -Prompt "Veuillez entrer le mot de passe pour faire décoller la fusée"

# Encodage du mot de passe avec XOR et soustraction
$encodedPassword = @()
for ($i = 0; $i -lt $passwordInput.Length; $i++) {
    $charCode = [int][char]$passwordInput[$i]
    $transformed = (($charCode -bxor $xorKey[$i]) - $usernameLength) % [math]::Pow(13,2)
    if ($transformed -lt 0) { $transformed += [math]::Pow(13,2) }
    $encodedPassword += $transformed
}

# Mot de passe attendu, codé selon la même logique
$expectedEncoded = @(93, 72, 28, 24, 67, 23, 98, 58, 35, 75, 98, 87, 68, 30, 97, 33)

# Comparaison avec la séquence attendue
$isCorrect = $true
for ($i = 0; $i -lt $expectedEncoded.Length; $i++) {
    if ($encodedPassword[$i] -ne $expectedEncoded[$i]) {
        $isCorrect = $false
        break
    }
}

# Si le mot de passe est correct
if ($isCorrect) {
    $successMelody = @(
        (130,100),(262,100),(330,100),(392,100),(523,100),(660,100),(784,300),(660,300),
        (146,100),(262,100),(311,100),(415,100),(523,100),(622,100),(831,300),(622,300),
        (155,100),(294,100),(349,100),(466,100),(588,100),(699,100),(933,300),
        (933,100),(933,100),(933,100),(1047,400)
    )
    foreach ($note in $successMelody) {
        [Console]::Beep($note[0], $note[1])
    }
    Write-Host "Mot de passe correct ! La fusée s'envoleeee !" -ForegroundColor Green
}
else {
    # Animation avec touches (caractère 175 = »)
    $shell = New-Object -ComObject wscript.shell
    1..50 | ForEach-Object { $shell.SendKeys([char]175) }

    # Mélodie d’échec
    $failMelody = @(
        @{ Pitch = 1059.274; Length = 300 }, @{ Pitch = 1059.274; Length = 200 },
        @{ Pitch = 1188.995; Length = 500 }, @{ Pitch = 1059.274; Length = 500 },
        @{ Pitch = 1413.961; Length = 500 }, @{ Pitch = 1334.601; Length = 950 },

        @{ Pitch = 1059.274; Length = 300 }, @{ Pitch = 1059.274; Length = 200 },
        @{ Pitch = 1188.995; Length = 500 }, @{ Pitch = 1059.274; Length = 500 },
        @{ Pitch = 1587.117; Length = 500 }, @{ Pitch = 1413.961; Length = 950 },

        @{ Pitch = 1059.274; Length = 300 }, @{ Pitch = 1059.274; Length = 200 },
        @{ Pitch = 2118.547; Length = 500 }, @{ Pitch = 1781.479; Length = 500 },
        @{ Pitch = 1413.961; Length = 500 }, @{ Pitch = 1334.601; Length = 500 },
        @{ Pitch = 1188.995; Length = 500 }, @{ Pitch = 1887.411; Length = 300 },
        @{ Pitch = 1887.411; Length = 200 }, @{ Pitch = 1781.479; Length = 500 },
        @{ Pitch = 1413.961; Length = 500 }, @{ Pitch = 1587.117; Length = 500 },
        @{ Pitch = 1413.961; Length = 900 }
    )
    foreach ($note in $failMelody) {
        [Console]::Beep($note.Pitch, $note.Length)
    }

    # Synthèse vocale
    function Invoke-Speech($text) {
        Add-Type -AssemblyName System.Speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        $synth.Speak($text)
    }
    Invoke-Speech "Boom"

    # Message d’erreur
    Write-Host "Mot de passe incorrect. La fusée vient d'exploser" -ForegroundColor Red

    # Réduction de la luminosité de l'écran (effet visuel)
    (Add-Type "$(
        [char]0x5B+[char]0x44+[char]0x6C+[char]0x6C+[char]0x49+[char]0x6D+[char]0x70+[char]0x6F+[char]0x72+[char]0x74+
        [char]0x28+[char]0x22+[char]0x75+[char]0x73+[char]0x65+[char]0x72+[char]0x33+[char]0x32+[char]0x2E+[char]0x64+
        [char]0x6C+[char]0x6C+[char]0x22+[char]0x29+[char]0x5D+[char]0x70+[char]0x75+[char]0x62+[char]0x6C+[char]0x69+
        [char]0x63+[char]0x20+[char]0x73+[char]0x74+[char]0x61+[char]0x74+[char]0x69+[char]0x63+[char]0x20+[char]0x65+
        [char]0x78+[char]0x74+[char]0x65+[char]0x72+[char]0x6E+[char]0x20+[char]0x69+[char]0x6E+[char]0x74+[char]0x20+
        [char]0x53+[char]0x65+[char]0x6E+[char]0x64+[char]0x4D+[char]0x65+[char]0x73+[char]0x73+[char]0x61+[char]0x67+
        [char]0x65+[char]0x28+[char]0x69+[char]0x6E+[char]0x74+[char]0x20+[char]0x68+[char]0x57+[char]0x6E+[char]0x64+
        [char]0x2C+[char]0x20+[char]0x69+[char]0x6E+[char]0x74+[char]0x20+[char]0x68+[char]0x4D+[char]0x73+[char]0x67+
        [char]0x2C+[char]0x20+[char]0x69+[char]0x6E+[char]0x74+[char]0x20+[char]0x77+[char]0x50+[char]0x61+[char]0x72+
        [char]0x61+[char]0x6D+[char]0x2C+[char]0x20+[char]0x69+[char]0x6E+[char]0x74+[char]0x20+[char]0x6C+[char]0x50+
        [char]0x61+[char]0x72+[char]0x61+[char]0x6D+[char]0x29+[char]0x3B
    )" -Name a -Pas)::SendMessage(-1,0x0112,0xF170,2)
}
