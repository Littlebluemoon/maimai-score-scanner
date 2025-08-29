// fast_capture.c
#include <windows.h>
#include <stdint.h>

__declspec(dllexport) uint64_t capture_address(HANDLE hProc, uintptr_t base, uintptr_t* offsets, int count) {
    uint64_t result = 0;

    while (result == 0) {
        uintptr_t temp = base;

        for (int i = 0; i < count; i++) {
            if (!ReadProcessMemory(hProc, (LPCVOID)temp, &temp, sizeof(temp), NULL)) {
                temp = 0;
                break;
            }
            temp += offsets[i];
        }

        // Check if valid AND fits in 6 bytes
        if (temp != 0 && temp >= 0x010000000000ULL && temp <= 0x700000000000ULL) {
            result = temp;
            break;
        }
    }

    return result;
}