;; An atom is written as such:
:atom
;; ^ Does nothing as it is not used.

; Atoms simply exist for their name.
; no atoms ever need to be created as
; one could simply imagine that all
; possible atoms already exist at once.
;
; When an atom is first used, it is assigned
; a location in memory based on some hash, and
; any future use of that same atom/atom-name will
; reference the same exact location in memory.
;
; Atoms are not strings, you can't change anything
; about them, to do that, simply use another atom.
; Two seperate identical strings will take up and be
; declared in different locations in memory, this is
; not true for atoms. Atoms will always use the same
; location in memory, there is no reason for the to
; do otherwise, (unlike with strings)
;
; Atoms must start with a colon, then an identifier
; string, just like symbols (but with a colon in front).
;
;    (One may think of atoms as bein used the same way
;     as ENUMS are, existing only for the purpose of
;     having a way to identify something)

(let (a :atom) (b :atom) (c :hello))
(if (= :atom :atom) (puts :true))
(if (= a b) (puts :true))
(if (= c a) (puts :false) (puts :true))

;; True and False are handled as just atoms in LISP.
;;   Any equality operation for instance will return an atom.
;;   Atoms :true and :false, are predefined

(puts)
(puts (= a b))
(puts (> 2 3))

(puts)

(if :true  (puts 1) (puts 0))
(if :false (puts 1) (puts 0))
(puts)
(unless :true  (puts 1) (puts 0))
(unless :false (puts 1) (puts 0))