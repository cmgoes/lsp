(define (f x y) (- x y))
(let (a 4) (b 6))
(puts (f a b))     ;; Same as (f 4 6)
(puts (f b a))

(define (adder n) (define (h m) (+ m n)))
(puts ((adder 1) 8))
(puts ((adder 8) 8))  ;; Currying isn't always so pretty

;; Naming the return function is useless, so we use a lambda:
(define (subber n) (lambda (m o) (- n m o)))
(let (result ((subber 2) 3 4)))  ;; result = 2-3-4 = -5

(puts result)

;; Lambdas can be used like defines, by assigning them
;;   to symbols using the (let ...) statement:
(let (divide (λ (a b) (/ a b)))) ;; λ is an alt. name for `lambda'
(puts (divide 5 9))

(let (add-two (-> (+ %1 2))))  ;; Shorthand syntax
(puts (add-two 3))

(apply f '(50 3))  ;; This applies a function f with arguments (2 3)
          ;; ^ This is the same as (f 50 3) (i.e. (- 50 3))
(puts _)

(puts (/ 4 3))  ;; Two integers divided will produce a float

(puts "\nFunctions/macros can also be printed:")
(puts +)
(puts ->)
(puts lambda)
(puts f)
(puts divide)