//go:build netbsd && arm
// +build netbsd,arm

// Code generated by cmd/cgo -godefs; DO NOT EDIT.
// cgo -godefs disk/types_netbsd.go

package disk

const (
	sizeOfStatvfs = 0xcc8
)

type (
	Statvfs struct {
		Flag         uint32
		Bsize        uint32
		Frsize       uint32
		Iosize       uint32
		Blocks       uint64
		Bfree        uint64
		Bavail       uint64
		Bresvd       uint64
		Files        uint64
		Ffree        uint64
		Favail       uint64
		Fresvd       uint64
		Syncreads    uint64
		Syncwrites   uint64
		Asyncreads   uint64
		Asyncwrites  uint64
		Fsidx        _Ctype_struct___0
		Fsid         uint32
		Namemax      uint32
		Owner        uint32
		Pad_cgo_0    [4]byte
		Spare        [4]uint64
		Fstypename   [32]uint8
		Mntonname    [1024]uint8
		Mntfromname  [1024]uint8
		Mntfromlabel [1024]uint8
	}
)

type _Ctype_struct___0 struct {
	FsidVal [2]int32
}
