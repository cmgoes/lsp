(define (zero? n) (= n 0))

(define (divisible? p q) (= (% p q) 0))

(define (sum l) (apply + l))

(define (floor n) (- n (% n 1)))
(define (ceil  n) (- (floor (- n))))

(define (// n d) (floor (/ n d)))