// SPDX-License-Identifier: BSD-3-Clause
//go:build openbsd && riscv64

// Code generated by cmd/cgo -godefs; DO NOT EDIT.
// cgo -godefs mem/types_openbsd.go

package mem

const (
	CTLVfs        = 10
	VfsGeneric    = 0
	VfsBcacheStat = 3
)

const (
	sizeOfBcachestats = 0x90
)

type Bcachestats struct {
	Numbufs       int64
	Numbufpages   int64
	Numdirtypages int64
	Numcleanpages int64
	Pendingwrites int64
	Pendingreads  int64
	Numwrites     int64
	Numreads      int64
	Cachehits     int64
	Busymapped    int64
	Dmapages      int64
	Highpages     int64
	Delwribufs    int64
	Kvaslots      int64
	Avail         int64
	Highflips     int64
	Highflops     int64
	Dmaflips      int64
}
