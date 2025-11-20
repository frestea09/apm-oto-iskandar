#include <GUIConstantsEx.au3>
#include <StaticConstants.au3>
#include <WindowsConstants.au3>
#include <MsgBoxConstants.au3>

Global Const $g_sConfigFile = @ScriptDir & "\\config.conf"
Global Const $g_sDefaultFristaPath = "D:\\BPJS\\Frista\\frista.exe"
Global Const $g_sDefaultAfterPath = "C:\\Program Files (x86)\\BPJS Kesehatan\\Aplikasi Sidik Jari BPJS Kesehatan\\After.exe"
Global Const $g_sDefaultChromePath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
Global Const $g_sDefaultChromeUrl = "http://172.168.1.175:8070"

Global $g_sFristaPath = $g_sDefaultFristaPath
Global $g_sAfterPath = $g_sDefaultAfterPath
Global $g_sChromePath = $g_sDefaultChromePath
Global $g_sChromeUrl = $g_sDefaultChromeUrl

Func _LoadPaths()
    $g_sFristaPath = IniRead($g_sConfigFile, "Paths", "FristaPath", $g_sDefaultFristaPath)
    $g_sAfterPath = IniRead($g_sConfigFile, "Paths", "AfterPath", $g_sDefaultAfterPath)
    $g_sChromePath = IniRead($g_sConfigFile, "Paths", "ChromePath", $g_sDefaultChromePath)
    $g_sChromeUrl = IniRead($g_sConfigFile, "Paths", "ChromeUrl", $g_sDefaultChromeUrl)
EndFunc

Func _EnsureValue($sValue, $sDefault)
    Local $sTrimmed = StringStripWS($sValue, 3)
    If $sTrimmed = "" Then
        Return $sDefault
    EndIf
    Return $sTrimmed
EndFunc

Func _PersistPaths($sFrista, $sAfter, $sChrome, $sUrl)
    $g_sFristaPath = _EnsureValue($sFrista, $g_sDefaultFristaPath)
    $g_sAfterPath = _EnsureValue($sAfter, $g_sDefaultAfterPath)
    $g_sChromePath = _EnsureValue($sChrome, $g_sDefaultChromePath)
    $g_sChromeUrl = _EnsureValue($sUrl, $g_sDefaultChromeUrl)

    IniWrite($g_sConfigFile, "Paths", "FristaPath", $g_sFristaPath)
    IniWrite($g_sConfigFile, "Paths", "AfterPath", $g_sAfterPath)
    IniWrite($g_sConfigFile, "Paths", "ChromePath", $g_sChromePath)
    IniWrite($g_sConfigFile, "Paths", "ChromeUrl", $g_sChromeUrl)
EndFunc

Func _BrowseAndFill($iInputId, $sTitle)
    Local $sCurrent = GUICtrlRead($iInputId)
    Local $sFolder = StringRegExpReplace($sCurrent, "^(.*[\\/]).*", "\\1")
    Local $sPath = FileOpenDialog($sTitle, $sFolder, "Executable (*.exe)")
    If @error Then
        Return
    EndIf
    GUICtrlSetData($iInputId, $sPath)
EndFunc

Func _ShowSection($aMainControls, $aSettingsControls, $bShowMain)
    Local $iStateMain = @SW_HIDE
    Local $iStateSettings = @SW_HIDE

    If $bShowMain Then
        $iStateMain = @SW_SHOW
    Else
        $iStateSettings = @SW_SHOW
    EndIf

    For $i = 0 To UBound($aMainControls) - 1
        GUICtrlSetState($aMainControls[$i], $iStateMain)
    Next

    For $i = 0 To UBound($aSettingsControls) - 1
        GUICtrlSetState($aSettingsControls[$i], $iStateSettings)
    Next
EndFunc

_LoadPaths()

; Membuat GUI fullscreen dengan style popup (tanpa border) untuk tampilan layar penuh
$hGUI = GUICreate("Mesin Layanan BPJS - Mudah Digunakan", @DesktopWidth, @DesktopHeight, 0, 0, $WS_POPUP)
GUISetBkColor(0xFFFFFF) ; Mengubah warna background GUI menjadi Putih
; Mengatur font yang lebih besar untuk aksesibilitas (sesuaikan jika perlu untuk layar besar)
GUISetFont(18, 400, 0, "Arial") ; Font diperbesar sedikit untuk fullscreen

$btnMenuLayanan = GUICtrlCreateButton("Menu Layanan", @DesktopWidth - 240, 20, 160, 40)
GUICtrlSetFont($btnMenuLayanan, 12, 800)
$btnMenuPengaturan = GUICtrlCreateButton("Pengaturan", @DesktopWidth - 240, 70, 160, 40)
GUICtrlSetFont($btnMenuPengaturan, 12, 800)

; Menambahkan logo rumah sakit (ganti "logo.png" dengan path file logo Anda, pastikan file ada di direktori script atau path lengkap)
; Logo ditempatkan di kiri atas untuk visibilitas
$logo = GUICtrlCreatePic("logo.jpg", 50, 20, 150, 100) ; Ukuran logo disesuaikan, ganti path jika perlu

; Label instruksi utama (posisi disesuaikan untuk memberi ruang logo)
$lblJudul = GUICtrlCreateLabel("Selamat datang di Mesin Layanan BPJS. Ikuti langkah-langkah berikut:", 220, 50, @DesktopWidth - 270, 60)
GUICtrlSetFont($lblJudul, 20, 800) ; Font lebih besar

; Label untuk input Nomor BPJS
$lblBpjs = GUICtrlCreateLabel("Masukkan Nomor BPJS Anda (16 digit):", 50, 140, @DesktopWidth - 100, 40)
$inputBPJS = GUICtrlCreateInput("", 50, 190, @DesktopWidth - 100, 60) ; Input field lebih besar
GUICtrlSetTip($inputBPJS, "Masukkan nomor BPJS tanpa spasi atau tanda baca")

; Label untuk input Nomor Booking
$lblBooking = GUICtrlCreateLabel("Masukkan Nomor Booking (jika ada):", 50, 270, @DesktopWidth - 100, 40)
$inputNomorBooking = GUICtrlCreateInput("", 50, 320, @DesktopWidth - 100, 60) ; Input field lebih besar
GUICtrlSetTip($inputNomorBooking, "Masukkan nomor booking jika Anda memiliki janji temu")

; Tombol untuk Login Frista (ukuran diperbesar untuk fullscreen)
$btnRun = GUICtrlCreateButton("1. Login dan Verifikasi Wajah (Frista)", 50, 400, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRun, 16, 800)
GUICtrlSetTip($btnRun, "Klik untuk login ke aplikasi Frista dan verifikasi wajah")

; Tombol untuk Pengisian Data BPJS
$btnRunPengisian = GUICtrlCreateButton("2. Isi Data Sidik Jari (Registrasi)", 50, 500, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRunPengisian, 16, 800)
GUICtrlSetTip($btnRunPengisian, "Klik untuk mengisi data sidik jari BPJS")

; Tombol untuk
$btnRunTiket = GUICtrlCreateButton("3. Print Tiket", 50, 600, @DesktopWidth - 100, 80)
GUICtrlSetFont($btnRunTiket, 16, 800)

; Label instruksi tambahan
$lblInstruksi = GUICtrlCreateLabel("Pastikan Anda memiliki kartu BPJS dan siap untuk verifikasi wajah atau sidik jari.", 50, 700, @DesktopWidth - 100, 50)
GUICtrlSetFont($lblInstruksi, 14, 400)

; Tombol Keluar (ditempatkan di bawah)
$btnExit = GUICtrlCreateButton("Keluar", 50, 750, @DesktopWidth - 100, 60)
GUICtrlSetFont($btnExit, 16, 800)
GUICtrlSetTip($btnExit, "Klik untuk menutup aplikasi")

; Footer: Label yang menjelaskan pembuat aplikasi
$lblFooter = GUICtrlCreateLabel("© 2025 SIMRS RSUD Otista Soreang", 50, 820, @DesktopWidth - 100, 40)
GUICtrlSetFont($lblFooter, 14, 400) ; Font lebih kecil untuk footer, tapi masih mudah dibaca
GUICtrlSetColor($lblFooter, 0x808080) ; Warna abu-abu untuk footer agar tidak terlalu mencolok

; Kontrol pengaturan
$lblPengaturan = GUICtrlCreateLabel("Pengaturan Lokasi Aplikasi", 50, 140, @DesktopWidth - 100, 40)
GUICtrlSetFont($lblPengaturan, 18, 800)

$lblFristaPath = GUICtrlCreateLabel("Lokasi Frista.exe", 50, 200, @DesktopWidth - 200, 30)
$inputFristaPath = GUICtrlCreateInput($g_sFristaPath, 50, 230, @DesktopWidth - 200, 40)
$btnBrowseFrista = GUICtrlCreateButton("Browse", @DesktopWidth - 130, 230, 80, 40)

$lblAfterPath = GUICtrlCreateLabel("Lokasi After.exe", 50, 290, @DesktopWidth - 200, 30)
$inputAfterPath = GUICtrlCreateInput($g_sAfterPath, 50, 320, @DesktopWidth - 200, 40)
$btnBrowseAfter = GUICtrlCreateButton("Browse", @DesktopWidth - 130, 320, 80, 40)

$lblChromePath = GUICtrlCreateLabel("Lokasi chrome.exe", 50, 380, @DesktopWidth - 200, 30)
$inputChromePath = GUICtrlCreateInput($g_sChromePath, 50, 410, @DesktopWidth - 200, 40)
$btnBrowseChrome = GUICtrlCreateButton("Browse", @DesktopWidth - 130, 410, 80, 40)

$lblChromeUrl = GUICtrlCreateLabel("URL pendaftaran online", 50, 470, @DesktopWidth - 200, 30)
$inputChromeUrl = GUICtrlCreateInput($g_sChromeUrl, 50, 500, @DesktopWidth - 200, 40)

$btnSaveSettings = GUICtrlCreateButton("Simpan Pengaturan", 50, 560, 250, 60)
GUICtrlSetFont($btnSaveSettings, 14, 800)

$lblInfoPengaturan = GUICtrlCreateLabel("Nilai default tetap tersimpan. Gunakan tombol Browse untuk memilih lokasi baru, lalu klik Simpan.", 50, 640, @DesktopWidth - 100, 60)
GUICtrlSetFont($lblInfoPengaturan, 12, 400)
GUICtrlSetColor($lblInfoPengaturan, 0x333333)

Global $g_aSectionMain[12] = [$logo, $lblJudul, $lblBpjs, $inputBPJS, $lblBooking, $inputNomorBooking, $btnRun, $btnRunPengisian, $btnRunTiket, $lblInstruksi, $btnExit, $lblFooter]
Global $g_aSectionSettings[14] = [$lblPengaturan, $lblFristaPath, $inputFristaPath, $btnBrowseFrista, $lblAfterPath, $inputAfterPath, $btnBrowseAfter, $lblChromePath, $inputChromePath, $btnBrowseChrome, $lblChromeUrl, $inputChromeUrl, $btnSaveSettings, $lblInfoPengaturan]

; Menampilkan GUI dalam mode fullscreen
GUISetState(@SW_SHOW)

_ShowSection($g_aSectionMain, $g_aSectionSettings, True)

While 1
    $nMsg = GUIGetMsg() ; Mengambil pesan dari GUI

    If $nMsg = $btnMenuLayanan Then
        _ShowSection($g_aSectionMain, $g_aSectionSettings, True)
    ElseIf $nMsg = $btnMenuPengaturan Then
        _ShowSection($g_aSectionMain, $g_aSectionSettings, False)
    EndIf

    ; Jika tombol "Login Frista" diklik
    If $nMsg = $btnRun Then
        $bpjsNumber = GUICtrlRead($inputBPJS)
        $bookingNumber = GUICtrlRead($inputNomorBooking) ; Baca nomor booking, meskipun belum digunakan di fungsi ini

        ; Validasi input
        ;If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
         ;   MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
          ;  ContinueLoop
        ;EndIf

        ; Menjalankan aplikasi Frista
        Run('"' & $g_sFristaPath & '"')
        Sleep(1000)

        ; Menunggu jendela Login Frista muncul dan aktif
        If Not WinWaitActive("Login Frista (Face Recognition BPJS Kesehatan)", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Aplikasi Frista tidak dapat dibuka. Hubungi petugas.")
            ContinueLoop
        EndIf

        $pos = WinGetPos("Login Frista (Face Recognition BPJS Kesehatan)")

        ; Mengisi username dan password
        Send("1002r006th") ; Username
        Send("{TAB}")      ; Pindah ke field password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")      ; Pindah ke tombol login
        Send("{SPACE}")    ; Klik tombol login

        ; Tunggu jendela utama Frista
        If Not WinWaitActive("Frista (Face Recognition BPJS Kesehatan)", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Login gagal. Coba lagi atau hubungi petugas.")
            ContinueLoop
        EndIf

        ; Kirim nomor BPJS
        Send($bpjsNumber)
        Sleep(1000)

        ; Tunggu jendela hasil pengenalan wajah
        If Not WinWaitActive("Hasil Pengenalan Wajah", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Verifikasi wajah gagal. Pastikan wajah terlihat jelas.")
            ContinueLoop
        EndIf

        ; Klik tombol "OK"
        ControlClick("Hasil Pengenalan Wajah", "", "Button1")

        ; Tutup jendela utama Frista
        WinClose("Frista (Face Recognition BPJS Kesehatan)")

        ; Pesan sukses
        MsgBox($MB_ICONINFORMATION, "Sukses", "Verifikasi wajah selesai. Silakan lanjutkan ke langkah berikutnya.")
    EndIf

    ; Jika tombol "Pengisian Data BPJS" diklik
    If $nMsg = $btnRunPengisian Then
        $bpjsNumber = GUICtrlRead($inputBPJS)
        $bookingNumber = GUICtrlRead($inputNomorBooking)

        ; Validasi input
       ; If StringLen($bpjsNumber) <> 16 Or Not StringIsDigit($bpjsNumber) Then
        ;    MsgBox($MB_ICONERROR, "Error", "Nomor BPJS harus 16 digit angka. Silakan coba lagi.")
        ;    ContinueLoop
        ;EndIf

        ; Jalankan aplikasi After.exe
        Run('"' & $g_sAfterPath & '"')
        Sleep(2000)

        ; Tunggu jendela aplikasi
        If Not WinWaitActive("Aplikasi Registrasi Sidik Jari", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Aplikasi Registrasi tidak dapat dibuka. Hubungi petugas.")
            ContinueLoop
        EndIf

        ; Login
        Send("1002r006th") ; Username
        Send("{TAB}")      ; Pindah ke password
        Send("{#}Bandung28") ; Password
        Send("{TAB}")      ; Pindah ke tombol login
        Send("{ENTER}")    ; Login
          Sleep(1000)
        ; Tunggu jendela utama
        If Not WinWaitActive("Aplikasi Registrasi Sidik Jari", "", 10) Then
            MsgBox($MB_ICONERROR, "Error", "Login gagal. Coba lagi atau hubungi petugas.")
            ContinueLoop
        EndIf

        ; Kirim nomor BPJS
        Send($bpjsNumber)
        Sleep(3000)

        ; Tutup aplikasi
        WinClose("Aplikasi Registrasi Sidik Jari")

        ; Pesan sukses
        MsgBox($MB_ICONINFORMATION, "Sukses", "Pengisian data sidik jari selesai. Terima kasih telah menggunakan layanan ini.")
    EndIf
  If $nMsg = $btnRunTiket Then
          ; Membuka URL di Google Chrome
          Run('"' & $g_sChromePath & '" ' & $g_sChromeUrl)
          Sleep(3000)  ; Tunggu beberapa detik untuk memastikan halaman terbuka

          ; Menunggu jendela dengan judul "PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG" aktif
          WinWaitActive("PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG - Google Chrome", "", 10)

          ; Klik tombol pendaftaran online (menggunakan koordinat yang diberikan)
          MouseClick("left", 773, 209)  ; Koordinat untuk klik pada tombol pendaftaran
          Sleep(2000)  ; Tunggu beberapa detik agar proses pendaftaran selesai

          ; Setelah proses pendaftaran selesai, menunggu jendela "Cetak Resume Pendaftaran Online"
          WinWaitActive("Cetak Resume Pendaftaran Online - Google Chrome", "", 10)

          ; Tekan Ctrl + P untuk membuka dialog cetak
          ;Send("^p")
          Sleep(3000)  ; Tunggu beberapa detik agar dialog cetak muncul

          ; Klik tombol Print di dialog (menggunakan koordinat yang diberikan)
          MouseClick("left", 373, 332)  ; Koordinat untuk klik tombol Print
          Sleep(2000)  ; Tunggu beberapa detik agar proses print selesai
          WinClose("PENDAFTARAN ONLINE : RSUD OTISTA BANDUNG - Google Chrome")
          ; Kembali ke aplikasi (opsional, jika perlu)
          ; WinActivate("Frista (Face Recognition BPJS Kesehatan)")  ; Jika Anda perlu kembali ke aplikasi lain
          MsgBox($MB_ICONINFORMATION, "Sukses", "Verifikasi wajah selesai. Silakan lanjutkan ke langkah berikutnya.")
  EndIf

    If $nMsg = $btnBrowseFrista Then
        _BrowseAndFill($inputFristaPath, "Pilih Frista.exe")
    ElseIf $nMsg = $btnBrowseAfter Then
        _BrowseAndFill($inputAfterPath, "Pilih After.exe")
    ElseIf $nMsg = $btnBrowseChrome Then
        _BrowseAndFill($inputChromePath, "Pilih chrome.exe")
    ElseIf $nMsg = $btnSaveSettings Then
        _PersistPaths(GUICtrlRead($inputFristaPath), GUICtrlRead($inputAfterPath), GUICtrlRead($inputChromePath), GUICtrlRead($inputChromeUrl))
        MsgBox($MB_ICONINFORMATION, "Tersimpan", "Pengaturan lokasi aplikasi berhasil disimpan.")
        _ShowSection($g_aSectionMain, $g_aSectionSettings, True)
    EndIf

    ; Jika tombol Keluar diklik
    If $nMsg = $btnExit Or $nMsg = $GUI_EVENT_CLOSE Then
        Exit
    EndIf
WEnd