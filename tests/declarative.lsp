;; Add 10 to every element of '(1 2 3 4).
(map (-> (+ %1 10)) '(1 2 3 4))
(puts _)

;; Partial harmonic sum:
; H_n = 1/1 + 1/2 + 1/3 + 1/4 + ... + 1/n
(define (H n)
  (reduce + 1 (map (λ (m) (/ 1 m)) (range 2 n))))

(let (n 20))
(print n "th Harmonic number = " (H n) "\n")

(define (factorial n)
  (reduce * 1 (range 2 n)))

((<> puts factorial) 6)