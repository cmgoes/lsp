(define (to_string node) (string node))
(define (to_atom   node) (name (to_string node)))
(define (to_bool   node) (if node :true :false))

(define (type? testee tester) (= (type testee) (name tester)))

(define (nil?  maybe) (type? maybe :Nil))
(define (atom? maybe) (type? maybe :Atom))