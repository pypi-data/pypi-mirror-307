//go:build windows

// Code generated by 'go generate' using "github.com/Microsoft/go-winio/tools/mkwinsyscall"; DO NOT EDIT.

package winio

import (
	"syscall"
	"unsafe"

	"golang.org/x/sys/windows"
)

var _ unsafe.Pointer

// Do the interface allocations only once for common
// Errno values.
const (
	errnoERROR_IO_PENDING = 997
)

var (
	errERROR_IO_PENDING error = syscall.Errno(errnoERROR_IO_PENDING)
	errERROR_EINVAL     error = syscall.EINVAL
)

// errnoErr returns common boxed Errno values, to prevent
// allocations at runtime.
func errnoErr(e syscall.Errno) error {
	switch e {
	case 0:
		return errERROR_EINVAL
	case errnoERROR_IO_PENDING:
		return errERROR_IO_PENDING
	}
	return e
}

var (
	modadvapi32 = windows.NewLazySystemDLL("advapi32.dll")
	modkernel32 = windows.NewLazySystemDLL("kernel32.dll")
	modntdll    = windows.NewLazySystemDLL("ntdll.dll")
	modws2_32   = windows.NewLazySystemDLL("ws2_32.dll")

	procAdjustTokenPrivileges              = modadvapi32.NewProc("AdjustTokenPrivileges")
	procConvertSidToStringSidW             = modadvapi32.NewProc("ConvertSidToStringSidW")
	procConvertStringSidToSidW             = modadvapi32.NewProc("ConvertStringSidToSidW")
	procImpersonateSelf                    = modadvapi32.NewProc("ImpersonateSelf")
	procLookupAccountNameW                 = modadvapi32.NewProc("LookupAccountNameW")
	procLookupAccountSidW                  = modadvapi32.NewProc("LookupAccountSidW")
	procLookupPrivilegeDisplayNameW        = modadvapi32.NewProc("LookupPrivilegeDisplayNameW")
	procLookupPrivilegeNameW               = modadvapi32.NewProc("LookupPrivilegeNameW")
	procLookupPrivilegeValueW              = modadvapi32.NewProc("LookupPrivilegeValueW")
	procOpenThreadToken                    = modadvapi32.NewProc("OpenThreadToken")
	procRevertToSelf                       = modadvapi32.NewProc("RevertToSelf")
	procBackupRead                         = modkernel32.NewProc("BackupRead")
	procBackupWrite                        = modkernel32.NewProc("BackupWrite")
	procCancelIoEx                         = modkernel32.NewProc("CancelIoEx")
	procConnectNamedPipe                   = modkernel32.NewProc("ConnectNamedPipe")
	procCreateIoCompletionPort             = modkernel32.NewProc("CreateIoCompletionPort")
	procCreateNamedPipeW                   = modkernel32.NewProc("CreateNamedPipeW")
	procDisconnectNamedPipe                = modkernel32.NewProc("DisconnectNamedPipe")
	procGetCurrentThread                   = modkernel32.NewProc("GetCurrentThread")
	procGetNamedPipeHandleStateW           = modkernel32.NewProc("GetNamedPipeHandleStateW")
	procGetNamedPipeInfo                   = modkernel32.NewProc("GetNamedPipeInfo")
	procGetQueuedCompletionStatus          = modkernel32.NewProc("GetQueuedCompletionStatus")
	procSetFileCompletionNotificationModes = modkernel32.NewProc("SetFileCompletionNotificationModes")
	procNtCreateNamedPipeFile              = modntdll.NewProc("NtCreateNamedPipeFile")
	procRtlDefaultNpAcl                    = modntdll.NewProc("RtlDefaultNpAcl")
	procRtlDosPathNameToNtPathName_U       = modntdll.NewProc("RtlDosPathNameToNtPathName_U")
	procRtlNtStatusToDosErrorNoTeb         = modntdll.NewProc("RtlNtStatusToDosErrorNoTeb")
	procWSAGetOverlappedResult             = modws2_32.NewProc("WSAGetOverlappedResult")
)

func adjustTokenPrivileges(token windows.Token, releaseAll bool, input *byte, outputSize uint32, output *byte, requiredSize *uint32) (success bool, err error) {
	var _p0 uint32
	if releaseAll {
		_p0 = 1
	}
	r0, _, e1 := syscall.SyscallN(procAdjustTokenPrivileges.Addr(), uintptr(token), uintptr(_p0), uintptr(unsafe.Pointer(input)), uintptr(outputSize), uintptr(unsafe.Pointer(output)), uintptr(unsafe.Pointer(requiredSize)))
	success = r0 != 0
	if true {
		err = errnoErr(e1)
	}
	return
}

func convertSidToStringSid(sid *byte, str **uint16) (err error) {
	r1, _, e1 := syscall.SyscallN(procConvertSidToStringSidW.Addr(), uintptr(unsafe.Pointer(sid)), uintptr(unsafe.Pointer(str)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func convertStringSidToSid(str *uint16, sid **byte) (err error) {
	r1, _, e1 := syscall.SyscallN(procConvertStringSidToSidW.Addr(), uintptr(unsafe.Pointer(str)), uintptr(unsafe.Pointer(sid)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func impersonateSelf(level uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procImpersonateSelf.Addr(), uintptr(level))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func lookupAccountName(systemName *uint16, accountName string, sid *byte, sidSize *uint32, refDomain *uint16, refDomainSize *uint32, sidNameUse *uint32) (err error) {
	var _p0 *uint16
	_p0, err = syscall.UTF16PtrFromString(accountName)
	if err != nil {
		return
	}
	return _lookupAccountName(systemName, _p0, sid, sidSize, refDomain, refDomainSize, sidNameUse)
}

func _lookupAccountName(systemName *uint16, accountName *uint16, sid *byte, sidSize *uint32, refDomain *uint16, refDomainSize *uint32, sidNameUse *uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procLookupAccountNameW.Addr(), uintptr(unsafe.Pointer(systemName)), uintptr(unsafe.Pointer(accountName)), uintptr(unsafe.Pointer(sid)), uintptr(unsafe.Pointer(sidSize)), uintptr(unsafe.Pointer(refDomain)), uintptr(unsafe.Pointer(refDomainSize)), uintptr(unsafe.Pointer(sidNameUse)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func lookupAccountSid(systemName *uint16, sid *byte, name *uint16, nameSize *uint32, refDomain *uint16, refDomainSize *uint32, sidNameUse *uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procLookupAccountSidW.Addr(), uintptr(unsafe.Pointer(systemName)), uintptr(unsafe.Pointer(sid)), uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(nameSize)), uintptr(unsafe.Pointer(refDomain)), uintptr(unsafe.Pointer(refDomainSize)), uintptr(unsafe.Pointer(sidNameUse)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func lookupPrivilegeDisplayName(systemName string, name *uint16, buffer *uint16, size *uint32, languageId *uint32) (err error) {
	var _p0 *uint16
	_p0, err = syscall.UTF16PtrFromString(systemName)
	if err != nil {
		return
	}
	return _lookupPrivilegeDisplayName(_p0, name, buffer, size, languageId)
}

func _lookupPrivilegeDisplayName(systemName *uint16, name *uint16, buffer *uint16, size *uint32, languageId *uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procLookupPrivilegeDisplayNameW.Addr(), uintptr(unsafe.Pointer(systemName)), uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(buffer)), uintptr(unsafe.Pointer(size)), uintptr(unsafe.Pointer(languageId)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func lookupPrivilegeName(systemName string, luid *uint64, buffer *uint16, size *uint32) (err error) {
	var _p0 *uint16
	_p0, err = syscall.UTF16PtrFromString(systemName)
	if err != nil {
		return
	}
	return _lookupPrivilegeName(_p0, luid, buffer, size)
}

func _lookupPrivilegeName(systemName *uint16, luid *uint64, buffer *uint16, size *uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procLookupPrivilegeNameW.Addr(), uintptr(unsafe.Pointer(systemName)), uintptr(unsafe.Pointer(luid)), uintptr(unsafe.Pointer(buffer)), uintptr(unsafe.Pointer(size)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func lookupPrivilegeValue(systemName string, name string, luid *uint64) (err error) {
	var _p0 *uint16
	_p0, err = syscall.UTF16PtrFromString(systemName)
	if err != nil {
		return
	}
	var _p1 *uint16
	_p1, err = syscall.UTF16PtrFromString(name)
	if err != nil {
		return
	}
	return _lookupPrivilegeValue(_p0, _p1, luid)
}

func _lookupPrivilegeValue(systemName *uint16, name *uint16, luid *uint64) (err error) {
	r1, _, e1 := syscall.SyscallN(procLookupPrivilegeValueW.Addr(), uintptr(unsafe.Pointer(systemName)), uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(luid)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func openThreadToken(thread windows.Handle, accessMask uint32, openAsSelf bool, token *windows.Token) (err error) {
	var _p0 uint32
	if openAsSelf {
		_p0 = 1
	}
	r1, _, e1 := syscall.SyscallN(procOpenThreadToken.Addr(), uintptr(thread), uintptr(accessMask), uintptr(_p0), uintptr(unsafe.Pointer(token)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func revertToSelf() (err error) {
	r1, _, e1 := syscall.SyscallN(procRevertToSelf.Addr())
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func backupRead(h windows.Handle, b []byte, bytesRead *uint32, abort bool, processSecurity bool, context *uintptr) (err error) {
	var _p0 *byte
	if len(b) > 0 {
		_p0 = &b[0]
	}
	var _p1 uint32
	if abort {
		_p1 = 1
	}
	var _p2 uint32
	if processSecurity {
		_p2 = 1
	}
	r1, _, e1 := syscall.SyscallN(procBackupRead.Addr(), uintptr(h), uintptr(unsafe.Pointer(_p0)), uintptr(len(b)), uintptr(unsafe.Pointer(bytesRead)), uintptr(_p1), uintptr(_p2), uintptr(unsafe.Pointer(context)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func backupWrite(h windows.Handle, b []byte, bytesWritten *uint32, abort bool, processSecurity bool, context *uintptr) (err error) {
	var _p0 *byte
	if len(b) > 0 {
		_p0 = &b[0]
	}
	var _p1 uint32
	if abort {
		_p1 = 1
	}
	var _p2 uint32
	if processSecurity {
		_p2 = 1
	}
	r1, _, e1 := syscall.SyscallN(procBackupWrite.Addr(), uintptr(h), uintptr(unsafe.Pointer(_p0)), uintptr(len(b)), uintptr(unsafe.Pointer(bytesWritten)), uintptr(_p1), uintptr(_p2), uintptr(unsafe.Pointer(context)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func cancelIoEx(file windows.Handle, o *windows.Overlapped) (err error) {
	r1, _, e1 := syscall.SyscallN(procCancelIoEx.Addr(), uintptr(file), uintptr(unsafe.Pointer(o)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func connectNamedPipe(pipe windows.Handle, o *windows.Overlapped) (err error) {
	r1, _, e1 := syscall.SyscallN(procConnectNamedPipe.Addr(), uintptr(pipe), uintptr(unsafe.Pointer(o)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func createIoCompletionPort(file windows.Handle, port windows.Handle, key uintptr, threadCount uint32) (newport windows.Handle, err error) {
	r0, _, e1 := syscall.SyscallN(procCreateIoCompletionPort.Addr(), uintptr(file), uintptr(port), uintptr(key), uintptr(threadCount))
	newport = windows.Handle(r0)
	if newport == 0 {
		err = errnoErr(e1)
	}
	return
}

func createNamedPipe(name string, flags uint32, pipeMode uint32, maxInstances uint32, outSize uint32, inSize uint32, defaultTimeout uint32, sa *windows.SecurityAttributes) (handle windows.Handle, err error) {
	var _p0 *uint16
	_p0, err = syscall.UTF16PtrFromString(name)
	if err != nil {
		return
	}
	return _createNamedPipe(_p0, flags, pipeMode, maxInstances, outSize, inSize, defaultTimeout, sa)
}

func _createNamedPipe(name *uint16, flags uint32, pipeMode uint32, maxInstances uint32, outSize uint32, inSize uint32, defaultTimeout uint32, sa *windows.SecurityAttributes) (handle windows.Handle, err error) {
	r0, _, e1 := syscall.SyscallN(procCreateNamedPipeW.Addr(), uintptr(unsafe.Pointer(name)), uintptr(flags), uintptr(pipeMode), uintptr(maxInstances), uintptr(outSize), uintptr(inSize), uintptr(defaultTimeout), uintptr(unsafe.Pointer(sa)))
	handle = windows.Handle(r0)
	if handle == windows.InvalidHandle {
		err = errnoErr(e1)
	}
	return
}

func disconnectNamedPipe(pipe windows.Handle) (err error) {
	r1, _, e1 := syscall.SyscallN(procDisconnectNamedPipe.Addr(), uintptr(pipe))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func getCurrentThread() (h windows.Handle) {
	r0, _, _ := syscall.SyscallN(procGetCurrentThread.Addr())
	h = windows.Handle(r0)
	return
}

func getNamedPipeHandleState(pipe windows.Handle, state *uint32, curInstances *uint32, maxCollectionCount *uint32, collectDataTimeout *uint32, userName *uint16, maxUserNameSize uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procGetNamedPipeHandleStateW.Addr(), uintptr(pipe), uintptr(unsafe.Pointer(state)), uintptr(unsafe.Pointer(curInstances)), uintptr(unsafe.Pointer(maxCollectionCount)), uintptr(unsafe.Pointer(collectDataTimeout)), uintptr(unsafe.Pointer(userName)), uintptr(maxUserNameSize))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func getNamedPipeInfo(pipe windows.Handle, flags *uint32, outSize *uint32, inSize *uint32, maxInstances *uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procGetNamedPipeInfo.Addr(), uintptr(pipe), uintptr(unsafe.Pointer(flags)), uintptr(unsafe.Pointer(outSize)), uintptr(unsafe.Pointer(inSize)), uintptr(unsafe.Pointer(maxInstances)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func getQueuedCompletionStatus(port windows.Handle, bytes *uint32, key *uintptr, o **ioOperation, timeout uint32) (err error) {
	r1, _, e1 := syscall.SyscallN(procGetQueuedCompletionStatus.Addr(), uintptr(port), uintptr(unsafe.Pointer(bytes)), uintptr(unsafe.Pointer(key)), uintptr(unsafe.Pointer(o)), uintptr(timeout))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func setFileCompletionNotificationModes(h windows.Handle, flags uint8) (err error) {
	r1, _, e1 := syscall.SyscallN(procSetFileCompletionNotificationModes.Addr(), uintptr(h), uintptr(flags))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}

func ntCreateNamedPipeFile(pipe *windows.Handle, access ntAccessMask, oa *objectAttributes, iosb *ioStatusBlock, share ntFileShareMode, disposition ntFileCreationDisposition, options ntFileOptions, typ uint32, readMode uint32, completionMode uint32, maxInstances uint32, inboundQuota uint32, outputQuota uint32, timeout *int64) (status ntStatus) {
	r0, _, _ := syscall.SyscallN(procNtCreateNamedPipeFile.Addr(), uintptr(unsafe.Pointer(pipe)), uintptr(access), uintptr(unsafe.Pointer(oa)), uintptr(unsafe.Pointer(iosb)), uintptr(share), uintptr(disposition), uintptr(options), uintptr(typ), uintptr(readMode), uintptr(completionMode), uintptr(maxInstances), uintptr(inboundQuota), uintptr(outputQuota), uintptr(unsafe.Pointer(timeout)))
	status = ntStatus(r0)
	return
}

func rtlDefaultNpAcl(dacl *uintptr) (status ntStatus) {
	r0, _, _ := syscall.SyscallN(procRtlDefaultNpAcl.Addr(), uintptr(unsafe.Pointer(dacl)))
	status = ntStatus(r0)
	return
}

func rtlDosPathNameToNtPathName(name *uint16, ntName *unicodeString, filePart uintptr, reserved uintptr) (status ntStatus) {
	r0, _, _ := syscall.SyscallN(procRtlDosPathNameToNtPathName_U.Addr(), uintptr(unsafe.Pointer(name)), uintptr(unsafe.Pointer(ntName)), uintptr(filePart), uintptr(reserved))
	status = ntStatus(r0)
	return
}

func rtlNtStatusToDosError(status ntStatus) (winerr error) {
	r0, _, _ := syscall.SyscallN(procRtlNtStatusToDosErrorNoTeb.Addr(), uintptr(status))
	if r0 != 0 {
		winerr = syscall.Errno(r0)
	}
	return
}

func wsaGetOverlappedResult(h windows.Handle, o *windows.Overlapped, bytes *uint32, wait bool, flags *uint32) (err error) {
	var _p0 uint32
	if wait {
		_p0 = 1
	}
	r1, _, e1 := syscall.SyscallN(procWSAGetOverlappedResult.Addr(), uintptr(h), uintptr(unsafe.Pointer(o)), uintptr(unsafe.Pointer(bytes)), uintptr(_p0), uintptr(unsafe.Pointer(flags)))
	if r1 == 0 {
		err = errnoErr(e1)
	}
	return
}
