//#############################################################################
//# Function: 2 Input Nand Gate                                               #
//# Copyright: Lambda Project Authors. All rights Reserved.                   #
//# License:  MIT (see LICENSE file in Lambda repository)                     #
//#############################################################################

module la_nand2 #(
    parameter PROP = "DEFAULT"
) (
    input  a,
    input  b,
    output z
);

    assign z = ~(a & b);

endmodule
