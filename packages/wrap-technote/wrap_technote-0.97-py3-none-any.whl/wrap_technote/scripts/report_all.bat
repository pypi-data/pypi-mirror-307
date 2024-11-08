call activate wrap
call wraptn waterlevels -s1 -s2 -s3 --static -r %1 -vv
call wraptn salinities -s4 -s5 -s6 -s7 --static -r %1 -vv
call wraptn rainfall --no-download %1 -vv
call wraptn summaries --no-nbs -r %1 -vv
