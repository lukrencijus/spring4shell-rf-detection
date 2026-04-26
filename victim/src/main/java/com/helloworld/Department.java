package com.helloworld;

import lombok.*;
import javax.persistence.*;

@NoArgsConstructor
@AllArgsConstructor
@Data
@Entity
@Table(name = "departments")
public class Department {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(name = "department_name")
    private String departmentName;
    
    @Column(name = "building")
    private String building;
    
    @Column(name = "email")
    private String email;
    
    @Column(name = "head_of_department")
    private String headOfDepartment;
}
