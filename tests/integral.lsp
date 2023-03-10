(let (dx 0.05))

;; f(x) = x^2 + 3x.
(define (f x) (+ (* 3 x) (* x x)))

;; Integral of f(x) from a to b.
(define (integ a b)
  (if (< a b)
    (+ (* dx (f a)) (integ (+ dx a) b))
    0))

;; Display the integral of f from 2 to 7
(puts (integ 2 7))


;; Result can be verified on Wolfram|Alpha
;; https://www.wolframalpha.com/input/?i=integral+(2+to+7)+(x%5E2+%2B+3x)dx